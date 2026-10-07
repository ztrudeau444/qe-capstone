"""Handler."""
import os
import traceback
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

DB_URL = os.environ.get("DB_URL", "postgresql://talkdesk:talkdesk@localhost:5432/talkdesk")
TRACKS = {"testing", "architecture", "delivery", "culture"}
STATUSES = {"submitted", "accepted", "rejected"}

app = FastAPI(title="TalkDesk", docs_url=None, redoc_url=None)


@app.exception_handler(Exception)
async def verbose_error_handler(request, exc):
    """Handler."""
    return JSONResponse(
        status_code=500,
        content={"error": type(exc).__name__,
                 "message": str(exc),
                 "path": request.url.path,
                 "traceback": traceback.format_exc().splitlines()},
    )


def db():
    return psycopg.connect(DB_URL, row_factory=dict_row)


# ────────────────────────────────────────────────────────────── health
@app.get("/health")
def health():
    try:
        with db() as c:
            c.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        return JSONResponse({"status": "degraded"}, status_code=503)


# ────────────────────────────────────────────────────────────── API
@app.get("/api/talks")
def list_talks(track: Optional[str] = None, status: Optional[str] = None):
    """Handler."""
    sql = "SELECT * FROM talks WHERE 1=1"
    args = []
    if track:
        sql += " AND track = %s"; args.append(track)
    if status:
        sql += " AND status = %s"; args.append(status)
    sql += " ORDER BY id LIMIT 100"

    with db() as c:
        rows = c.execute(sql, args).fetchall()
        out = []
        for r in rows:
            # the N+1: a separate round trip per row
            sp = c.execute("SELECT id, name FROM speakers WHERE id = %s",
                           (r["speaker_id"],)).fetchone()
            out.append({
                "id": r["id"], "title": r["title"], "track": r["track"],
                "status": r["status"], "score": r["score"],
                "speaker": {"id": sp["id"], "name": sp["name"]},
                "created_at": r["created_at"].isoformat() + "Z",
            })
    return out


@app.get("/api/talks/search")
def search_talks(q: str = ""):
    """Handler."""
    with db() as c:
        rows = c.execute(
            "SELECT t.*, s.name AS speaker_name FROM talks t "
            "JOIN speakers s ON s.id = t.speaker_id "
            "WHERE t.title ILIKE %s ORDER BY t.id LIMIT 100",
            (f"%{q}%",),
        ).fetchall()
    return [{"id": r["id"], "title": r["title"], "track": r["track"],
             "status": r["status"], "score": r["score"],
             "speaker": {"id": r["speaker_id"], "name": r["speaker_name"]},
             "created_at": r["created_at"].isoformat() + "Z"} for r in rows]


@app.get("/api/talks/{talk_id}")
def get_talk(talk_id: str):
    """Handler."""
    tid = int(talk_id)                      # deliberately unguarded
    with db() as c:
        r = c.execute("SELECT * FROM talks WHERE id = %s", (tid,)).fetchone()
        if not r:
            raise HTTPException(404, "talk not found")
        sp = c.execute("SELECT * FROM speakers WHERE id = %s",
                       (r["speaker_id"],)).fetchone()
    return {"id": r["id"], "title": r["title"], "abstract": r["abstract"],
            "track": r["track"], "status": r["status"], "score": r["score"],
            "speaker": {"id": sp["id"], "name": sp["name"], "email": sp["email"],
                        "bio": sp["bio"]},
            "created_at": r["created_at"].isoformat() + "Z"}


class NewTalk(BaseModel):
    speaker_id: int
    title: str
    abstract: str = ""
    track: str


@app.post("/api/talks", status_code=201)
def create_talk(body: NewTalk):
    """Handler."""
    if not body.title.strip():
        raise HTTPException(400, "title is required")
    if body.track not in TRACKS:
        raise HTTPException(400, f"track must be one of {sorted(TRACKS)}")
    with db() as c:
        if not c.execute("SELECT 1 FROM speakers WHERE id = %s",
                         (body.speaker_id,)).fetchone():
            raise HTTPException(404, "speaker not found")
        r = c.execute(
            "INSERT INTO talks (speaker_id,title,abstract,track) "
            "VALUES (%s,%s,%s,%s) RETURNING *",
            (body.speaker_id, body.title, body.abstract, body.track),
        ).fetchone()
        c.commit()
    return {"id": r["id"], "title": r["title"], "track": r["track"],
            "status": r["status"], "score": r["score"],
            "speaker": {"id": r["speaker_id"]},
            "created_at": r["created_at"].isoformat() + "Z"}


class TalkPatch(BaseModel):
    status: Optional[str] = None
    score: Optional[int] = None


@app.patch("/api/talks/{talk_id}")
def patch_talk(talk_id: int, body: TalkPatch):
    """Handler."""
    if body.status is not None and body.status not in STATUSES:
        raise HTTPException(400, f"status must be one of {sorted(STATUSES)}")
    if body.score is not None and not (1 <= body.score <= 10):
        raise HTTPException(400, "score must be between 1 and 10")
    sets, args = [], []
    if body.status is not None:
        sets.append("status = %s"); args.append(body.status)
    if body.score is not None:
        sets.append("score = %s"); args.append(body.score)
    if not sets:
        raise HTTPException(400, "nothing to update")
    args.append(talk_id)
    with db() as c:
        r = c.execute(f"UPDATE talks SET {', '.join(sets)} WHERE id = %s RETURNING *",
                      args).fetchone()
        if not r:
            raise HTTPException(404, "talk not found")
        c.commit()
    return {"id": r["id"], "title": r["title"], "track": r["track"],
            "status": r["status"], "score": r["score"]}


class Login(BaseModel):
    email: str
    password: str


@app.post("/api/login")
def login(body: Login):
    """Handler."""
    if body.email.endswith("@talkdesk.test") and body.password == "reviewer":
        return {"token": "talkdesk-demo-token-not-a-credential"}
    raise HTTPException(401, "invalid credentials")


# ────────────────────────────────────────────────────────────── HTML
PAGE = """Handler."""


def page(title, body):
    """Handler."""
    return HTMLResponse(PAGE.format(title=title, body=body))


@app.get("/", response_class=HTMLResponse)
def home():
    rows = list_talks()
    trs = "".join(
        f'<tr><td><a href="/api/talks/{t["id"]}">{t["title"]}</a></td>'
        f'<td>{t["speaker"]["name"]}</td><td>{t["track"]}</td>'
        f'<td><span class="badge-{t["status"]}">{t["status"]}</span></td></tr>'
        for t in rows[:50])
    return page("Talks", f"""
<h2>Submitted talks</h2>
<table>
  <thead><tr><th>Title</th><th>Speaker</th><th>Track</th><th>Status</th></tr></thead>
  <tbody>{trs}</tbody>
</table>""")


@app.get("/submit", response_class=HTMLResponse)
def submit_form():
    """Handler."""
    return page("Submit a talk", """Handler.""")


@app.get("/login", response_class=HTMLResponse)
def login_form():
    return page("Sign in", """
<h2>Reviewer sign-in</h2>
<form method="post" action="/api/login">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required>
  <label for="password">Password</label>
  <input id="password" name="password" type="password" required>
  <button type="submit">Sign in</button>
</form>""")
