"""HTTP boundary tests for the activation queue."""

from __future__ import annotations

import http.client
import json
import runpy
import socket
import sys
import threading
import types
from collections.abc import Iterator
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from scripts import serve

TEST_RELATIONSHIPS = [
    {
        "id": "rel-001",
        "from_party": "Account Alpha",
        "to_party": "Contact One",
        "kind": "partner",
        "next_move": "Confirm the next review date",
        "due": "2026-08-28",
        "why_now": "A test-only follow-up is due.",
        "status": "due",
    },
    {
        "id": "rel-002",
        "from_party": "Account Beta",
        "to_party": "Contact Two",
        "kind": "advisor",
        "next_move": "Share the bounded product note",
        "due": "2026-08-29",
        "why_now": "A test-only advisory review is scheduled.",
        "status": "due",
    },
    {
        "id": "rel-003",
        "from_party": "Account Gamma",
        "to_party": "Contact Three",
        "kind": "account-contact",
        "next_move": "Confirm the next check-in owner",
        "due": "2026-08-27",
        "why_now": "A test-only check-in is overdue.",
        "status": "due",
    },
]


@pytest.fixture
def http_server(monkeypatch: pytest.MonkeyPatch) -> Iterator[tuple[str, int]]:
    monkeypatch.setattr(serve, "QUEUE", serve.ActivationQueue(TEST_RELATIONSHIPS))
    server = ThreadingHTTPServer(("127.0.0.1", 0), serve.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield str(host), int(port)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def request(
    host: str,
    port: int,
    method: str,
    path: str,
    *,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection(host, port, timeout=2)
    try:
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read()
    finally:
        connection.close()


def post_raw(host: str, port: int, content_length: str, body: bytes) -> tuple[int, dict[str, str]]:
    raw_request = (
        "POST /api/queue/rel-001 HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii") + body
    with socket.create_connection((host, port), timeout=2) as connection:
        connection.sendall(raw_request)
        connection.shutdown(socket.SHUT_WR)
        response = bytearray()
        while chunk := connection.recv(65536):
            response.extend(chunk)
    head, payload = bytes(response).split(b"\r\n\r\n", 1)
    status = int(head.splitlines()[0].split()[1])
    return status, json.loads(payload.decode("utf-8"))


def test_default_runtime_queue_starts_empty() -> None:
    """Production startup must never consume bundled synthetic/demo records."""

    assert serve.QUEUE.home() == []


def test_get_home_serves_html_without_cache(http_server: tuple[str, int]) -> None:
    status, headers, body = request(*http_server, "GET", "/")
    assert status == 200
    assert headers["Cache-Control"] == "no-store"
    assert headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"ELUNVERA" in body
    assert b'type="module" src="/web/bootstrap.js"' in body


def test_get_index_alias_serves_actionable_accessible_empty_state(
    http_server: tuple[str, int],
) -> None:
    status, _, body = request(*http_server, "GET", "/index.html")
    assert status == 200
    assert b"Activation queue" in body
    assert b"No relationships are available yet." in body
    assert b'aria-live="polite"' in body
    assert b'role="status"' in body
    for internal_name in (b"LineageWeave", b"RankWeave", b"Ontology/SDP", b"Orgmetra"):
        assert internal_name not in body


@pytest.mark.parametrize(
    ("path", "content_type", "marker"),
    [
        ("/web/styles.css", "text/css; charset=utf-8", b"body"),
        ("/web/bootstrap.js", "text/javascript; charset=utf-8", b"createActivationApp"),
        ("/web/app.js", "text/javascript; charset=utf-8", b"createActivationApp"),
    ],
)
def test_get_serves_only_required_web_assets(
    http_server: tuple[str, int], path: str, content_type: str, marker: bytes
) -> None:
    status, headers, body = request(*http_server, "GET", path)
    assert status == 200
    assert headers["Content-Type"] == content_type
    assert headers["Cache-Control"] == "no-store"
    assert marker in body


@pytest.mark.parametrize(
    "path",
    ["/README.md", "/docs/prd.md", "/requirements-ci.txt", "/.github/workflows/ci.yml"],
)
def test_get_never_serves_repository_internal_files(
    http_server: tuple[str, int], path: str
) -> None:
    status, _, _ = request(*http_server, "GET", path)
    assert status == 404


@pytest.mark.parametrize(
    ("path", "content_type"),
    [
        ("/", "text/html; charset=utf-8"),
        ("/web/styles.css", "text/css; charset=utf-8"),
        ("/web/bootstrap.js", "text/javascript; charset=utf-8"),
        ("/api/queue", "application/json; charset=utf-8"),
    ],
)
def test_head_mirrors_only_allowed_get_surface_without_a_body(
    http_server: tuple[str, int], path: str, content_type: str
) -> None:
    status, headers, body = request(*http_server, "HEAD", path)
    assert status == 200
    assert headers["Content-Type"] == content_type
    assert headers["Cache-Control"] == "no-store"
    assert int(headers["Content-Length"]) >= 0
    assert body == b""


@pytest.mark.parametrize("path", ["/README.md", "/docs/prd.md", "/requirements-ci.txt"])
def test_head_never_exposes_repository_internal_files(
    http_server: tuple[str, int], path: str
) -> None:
    status, _, body = request(*http_server, "HEAD", path)
    assert status == 404
    assert body == b""


def test_get_queue_returns_relationships(http_server: tuple[str, int]) -> None:
    status, headers, body = request(*http_server, "GET", "/api/queue")
    assert status == 200
    assert headers["Content-Type"] == "application/json; charset=utf-8"
    payload = json.loads(body)
    assert payload["relationships"][0]["id"] == "rel-003"


def test_unknown_get_returns_404(http_server: tuple[str, int]) -> None:
    status, _, _ = request(*http_server, "GET", "/does-not-exist")
    assert status == 404


def test_unknown_post_path_returns_404(http_server: tuple[str, int]) -> None:
    status, _, _ = request(*http_server, "POST", "/api/not-queue", body=b"{}")
    assert status == 404


def test_post_applies_valid_action(http_server: tuple[str, int]) -> None:
    body = json.dumps({"action": "activate"}).encode("utf-8")
    status, headers, payload = request(
        *http_server,
        "POST",
        "/api/queue/rel-001",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    assert status == 200
    assert headers["Cache-Control"] == "no-store"
    assert json.loads(payload)["status"] == "activated"


def test_post_returns_json_for_domain_error(http_server: tuple[str, int]) -> None:
    body = json.dumps({"action": "activate"}).encode("utf-8")
    status, _, payload = request(
        *http_server,
        "POST",
        "/api/queue/rel-missing",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    assert status == 400
    assert "unknown relationship" in json.loads(payload)["error"]


def test_post_with_empty_body_returns_json_error(http_server: tuple[str, int]) -> None:
    status, _, payload = request(*http_server, "POST", "/api/queue/rel-001", body=b"")
    assert status == 400
    assert "unknown action" in json.loads(payload)["error"]


@pytest.mark.parametrize(
    ("content_length", "body"),
    [
        ("not-an-integer", b"{}"),
        ("-1", b""),
        (str(serve.MAX_REQUEST_BODY_BYTES + 1), b"{}"),
    ],
)
def test_post_rejects_invalid_content_length_as_json(
    http_server: tuple[str, int], content_length: str, body: bytes
) -> None:
    status, payload = post_raw(*http_server, content_length, body)
    assert status == 400
    assert "Content-Length" in payload["error"]


@pytest.mark.parametrize("body", [b"{", b"[]", b'"text"', b"\xff"])
def test_post_rejects_invalid_or_non_object_json(
    http_server: tuple[str, int], body: bytes
) -> None:
    status, payload = post_raw(*http_server, str(len(body)), body)
    assert status == 400
    assert payload == {"error": "request body must be a valid JSON object"}


def test_main_constructs_loopback_server_and_serves(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    observed: dict[str, Any] = {}

    class FakeServer:
        def __init__(self, address: tuple[str, int], handler: type[serve.Handler]) -> None:
            observed["address"] = address
            observed["handler"] = handler

        def serve_forever(self) -> None:
            observed["served"] = True

    monkeypatch.setattr(serve, "ThreadingHTTPServer", FakeServer)
    serve.main()
    assert observed == {
        "address": ("127.0.0.1", 8765),
        "handler": serve.Handler,
        "served": True,
    }
    assert "http://127.0.0.1:8765/" in capsys.readouterr().out


def test_module_entrypoint_calls_main(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: dict[str, Any] = {}

    class FakeServer:
        def __init__(self, address: tuple[str, int], handler: type[SimpleHTTPRequestHandler]) -> None:
            observed["address"] = address
            observed["handler"] = handler

        def serve_forever(self) -> None:
            observed["served"] = True

    fake_http_server = types.ModuleType("http.server")
    fake_http_server.SimpleHTTPRequestHandler = SimpleHTTPRequestHandler
    fake_http_server.ThreadingHTTPServer = FakeServer
    monkeypatch.setitem(sys.modules, "http.server", fake_http_server)
    runpy.run_path(str(Path(serve.__file__)), run_name="__main__")
    assert observed["address"] == ("127.0.0.1", 8765)
    assert observed["served"] is True
