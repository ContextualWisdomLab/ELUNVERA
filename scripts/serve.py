#!/usr/bin/env python3
"""Serve the ELUNVERA activation queue on http://127.0.0.1:8765/."""

from __future__ import annotations

import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from elunvera import ActivationQueue  # noqa: E402

# Runtime starts without fabricated customer relationships. Tests inject
# anonymized fixtures explicitly; a durable real-data repository is a later slice.
QUEUE = ActivationQueue(())
MAX_REQUEST_BODY_BYTES = 64 * 1024


class Handler(SimpleHTTPRequestHandler):
    """Serve static assets and the bounded activation-queue JSON API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        """Write one standard-library request log line to standard error."""

        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_GET(self) -> None:  # noqa: N802
        """Serve the home document, queue representation, or static fallback."""

        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            return self._file(ROOT / "web" / "index.html", "text/html; charset=utf-8")
        if parsed.path == "/api/queue":
            body = json.dumps(
                {"relationships": [row.to_dict() for row in QUEUE.home()]},
                ensure_ascii=False,
            ).encode("utf-8")
            return self._bytes(200, "application/json; charset=utf-8", body)
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        """Validate and apply one bounded relationship action."""

        parsed = urlparse(self.path)
        prefix = "/api/queue/"
        if not parsed.path.startswith(prefix):
            self.send_error(404)
            return
        relationship_id = parsed.path[len(prefix) :]
        try:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise ValueError("Content-Length must be an integer") from exc
            if not 0 <= length <= MAX_REQUEST_BODY_BYTES:
                raise ValueError(
                    f"Content-Length must be between 0 and {MAX_REQUEST_BODY_BYTES} bytes"
                )
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ValueError("request body must be a valid JSON object") from exc
            if not isinstance(payload, dict):
                raise ValueError("request body must be a valid JSON object")
            row = QUEUE.apply(
                relationship_id,
                str(payload.get("action", "")),
                due=payload.get("due"),
            )
        except (KeyError, ValueError) as exc:
            self._bytes(
                400,
                "application/json; charset=utf-8",
                json.dumps({"error": str(exc)}).encode(),
            )
            return
        self._bytes(
            200,
            "application/json; charset=utf-8",
            json.dumps(row.to_dict(), ensure_ascii=False).encode(),
        )

    def _file(self, path: Path, content_type: str) -> None:
        data = path.read_bytes()
        self._bytes(200, content_type, data)

    def _bytes(self, code: int, content_type: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    """Run the loopback-only multithreaded prototype server."""

    host, port = "127.0.0.1", 8765
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"ELUNVERA activation queue → http://{host}:{port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
