#!/usr/bin/env python3
"""The smallest thing that makes the pipeline demonstrable.

This is NOT your System Under Test and it is not a statement about what
language you should write in. It exists so that `docker compose up -d --wait`
succeeds on Week 0 Day 1, so the Week 3 stages have something to point at, and
so the smoke stage has a health endpoint to call — before you have written
anything.

Delete it, and this line from the Dockerfile, as soon as your own application
can do those three things.

Standard library only, deliberately: a placeholder with a dependency file is a
placeholder that can break.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type):
        payload = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path.rstrip("/") in ("/health", "/healthz"):
            self._send(200, json.dumps({"status": "ok", "placeholder": True}),
                       "application/json")
        elif self.path == "/":
            self._send(200,
                       "<!doctype html><title>Placeholder</title>"
                       "<h1>Replace me</h1><p>This is the starter's placeholder "
                       "application. Your System Under Test goes here.</p>",
                       "text/html; charset=utf-8")
        else:
            self._send(404, json.dumps({"error": "not found"}),
                       "application/json")

    def log_message(self, fmt, *args):      # quiet; CI logs are noisy enough
        pass


if __name__ == "__main__":
    print(f"placeholder listening on :{PORT} — replace this with your SUT",
          flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
