"""Product tests for the activation queue — not a 3-second stub."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from elunvera import ActivationQueue

SEED = Path(__file__).resolve().parents[1] / "data" / "activations.json"


def load_queue() -> ActivationQueue:
    payload = json.loads(SEED.read_text(encoding="utf-8"))
    return ActivationQueue(payload["relationships"])


def test_home_is_due_first_not_a_graph() -> None:
    home = load_queue().home()
    assert [row.id for row in home] == ["rel-003", "rel-001", "rel-002", "rel-004"]
    assert all(row.status in {"due", "rescheduled"} for row in home)
    assert not hasattr(ActivationQueue, "add_edge")
    assert not hasattr(ActivationQueue, "nodes")


def test_activate_leaves_the_home_queue() -> None:
    queue = load_queue()
    done = queue.apply("rel-003", "activate")
    assert done.status == "activated"
    assert "rel-003" not in {row.id for row in queue.home()}


def test_reschedule_keeps_row_with_new_due() -> None:
    queue = load_queue()
    moved = queue.apply("rel-001", "reschedule", due="2026-09-10")
    assert moved.status == "rescheduled"
    assert moved.due == "2026-09-10"
    home_ids = [row.id for row in queue.home()]
    assert home_ids[-1] == "rel-001"


def test_dismiss_leaves_home_without_deleting_identity() -> None:
    queue = load_queue()
    gone = queue.apply("rel-002", "dismiss")
    assert gone.status == "dismissed"
    assert queue.get("rel-002").id == "rel-002"
    assert "rel-002" not in {row.id for row in queue.home()}


def test_rejects_employment_or_lineage_kinds() -> None:
    with pytest.raises(ValueError, match="kind"):
        ActivationQueue(
            [
                {
                    "id": "rel-x",
                    "from_party": "A",
                    "to_party": "B",
                    "kind": "employment",
                    "next_move": "n/a",
                    "due": "2026-08-27",
                    "why_now": "n/a",
                    "status": "due",
                }
            ]
        )


def test_lineage_cite_is_optional_and_not_an_edge() -> None:
    row = load_queue().get("rel-001")
    assert row.lineage_cite is None
    dumped = row.to_dict()
    assert "edges" not in dumped
    assert "graph" not in dumped
