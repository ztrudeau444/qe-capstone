# TalkDesk (Python / FastAPI) — the System Under Test.
# python:3.12 because TalkDesk's pinned packages are built for it.
FROM python:3.12-slim
WORKDIR /app
COPY src/talkdesk/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/talkdesk/app.py .
RUN adduser --disabled-password --gecos "" app && chown -R app /app
USER app
EXPOSE 8080

# The slim image has no wget or curl, so the healthcheck uses Python itself.
# /health returns 503 when the database is unreachable, which fails this check.
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=10 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
