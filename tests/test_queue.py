"""Product tests for the activation queue using anonymized test-only fixtures."""

from __future__ import annotations

import pytest

from elunvera import ActivationQueue

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
    {
        "id": "rel-004",
        "from_party": "Account Delta",
        "to_party": "Contact Four",
        "kind": "collaborator",
        "next_move": "Review the next collaboration step",
        "due": "2026-08-30",
        "why_now": "A test-only collaboration review is scheduled.",
        "status": "rescheduled",
    },
]


def load_queue() -> ActivationQueue:
    """Build a fresh queue from anonymized unit-test fixtures."""

    return ActivationQueue(TEST_RELATIONSHIPS)


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
                    "from_party": "Account Test",
                    "to_party": "Contact Test",
                    "kind": "employment",
                    "next_move": "Not applicable",
                    "due": "2026-08-27",
                    "why_now": "A test-only invalid boundary case.",
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


@pytest.mark.parametrize("due", [1, ["2026-09-10"], {"date": "2026-09-10"}])
def test_reschedule_rejects_truthy_non_string_due(due: object) -> None:
    """Public callers receive a domain ValueError instead of a type leak."""

    queue = load_queue()
    with pytest.raises(ValueError, match="due date must be a string"):
        queue.apply("rel-001", "reschedule", due=due)  # type: ignore[arg-type]


def test_parse_preserves_lineage_citation_and_defaults_status() -> None:
    queue = ActivationQueue(
        [
            {
                "id": "rel-cited",
                "from_party": "Account Citation",
                "to_party": "Contact Citation",
                "kind": "collaborator",
                "next_move": "Review evidence",
                "due": "2026-09-10",
                "why_now": "Test-only evidence arrived.",
                "lineage_cite": "urn:lineage:test-node:1",
            }
        ]
    )
    row = queue.get("rel-cited")
    assert row.status == "due"
    assert row.to_dict()["lineage_cite"] == "urn:lineage:test-node:1"


def test_get_rejects_unknown_relationship() -> None:
    with pytest.raises(KeyError, match="unknown relationship rel-missing"):
        load_queue().get("rel-missing")


def test_apply_rejects_unknown_action() -> None:
    with pytest.raises(ValueError, match="unknown action"):
        load_queue().apply("rel-001", "archive")


@pytest.mark.parametrize("due", [None, ""])
def test_reschedule_requires_due_date(due: str | None) -> None:
    with pytest.raises(ValueError, match="reschedule requires a due date"):
        load_queue().apply("rel-001", "reschedule", due=due)


def test_reschedule_rejects_invalid_iso_date() -> None:
    with pytest.raises(ValueError, match="(Invalid isoformat|out of range)"):
        load_queue().apply("rel-001", "reschedule", due="2026-02-30")
