#!/usr/bin/env python3
"""Serve the ELUNVERA activation queue on http://127.0.0.1:8765/"""

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

SEED = json.loads((ROOT / "data" / "activations.json").read_text(encoding="utf-8"))
QUEUE = ActivationQueue(SEED["relationships"])


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_GET(self) -> None:  # noqa: N802
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
        parsed = urlparse(self.path)
        prefix = "/api/queue/"
        if not parsed.path.startswith(prefix):
            self.send_error(404)
            return
        relationship_id = parsed.path[len(prefix) :]
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        try:
            row = QUEUE.apply(
                relationship_id,
                str(payload.get("action", "")),
                due=payload.get("due"),
            )
        except (KeyError, ValueError) as exc:
            self._bytes(400, "application/json; charset=utf-8", json.dumps({"error": str(exc)}).encode())
            return
        self._bytes(200, "application/json; charset=utf-8", json.dumps(row.to_dict(), ensure_ascii=False).encode())

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
    host, port = "127.0.0.1", 8765
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"ELUNVERA activation queue → http://{host}:{port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
