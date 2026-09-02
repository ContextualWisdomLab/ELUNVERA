"""Activation queue: next move on a known relationship.

This module must not grow graph edges, retrieval ranking, catalog types,
or employment records. Optional `lineage_cite` is a foreign identifier, never an edge.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Iterable, Mapping

ALLOWED_KINDS = frozenset({"partner", "advisor", "account-contact", "collaborator"})
HOME_STATUSES = frozenset({"due", "rescheduled"})
TERMINAL_STATUSES = frozenset({"activated", "dismissed"})
VALID_STATUSES = HOME_STATUSES | TERMINAL_STATUSES
ACTIONS = frozenset({"activate", "reschedule", "dismiss"})


@dataclass(frozen=True)
class Relationship:
    """One tenant-local relationship and its next evidence-backed move."""

    relationship_id: str
    from_party: str
    to_party: str
    kind: str
    next_move: str
    due: str
    why_now: str
    status: str
    lineage_cite: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the stable JSON-ready representation used by the HTTP boundary."""

        data = asdict(self)
        if data["lineage_cite"] is None:
            data.pop("lineage_cite")
        return data


class ActivationQueue:
    """Manage the bounded home queue without owning graph or employment truth."""

    def __init__(self, items: Iterable[Mapping[str, Any]]) -> None:
        self._rows: dict[str, Relationship] = {}
        for raw in items:
            row = self._parse(raw)
            if row.kind not in ALLOWED_KINDS:
                raise ValueError(f"kind {row.kind!r} is not an ELUNVERA relationship kind")
            if row.relationship_id in self._rows:
                raise ValueError(f"duplicate relationship_id {row.relationship_id}")
            self._rows[row.relationship_id] = row

    @staticmethod
    def _parse(raw: Mapping[str, Any]) -> Relationship:
        relationship_id = raw["relationship_id"]
        if not isinstance(relationship_id, str) or not relationship_id.strip():
            raise ValueError("relationship_id must be a non-empty string")

        text_values: dict[str, str] = {}
        for field_name in ("from_party", "to_party", "kind", "next_move", "why_now"):
            field_value = raw[field_name]
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
            text_values[field_name] = field_value

        due = raw["due"]
        if not isinstance(due, str) or not due:
            raise ValueError("due must be a non-empty ISO date string")
        try:
            date.fromisoformat(due)
        except ValueError as exc:
            raise ValueError("due must be a valid ISO date") from exc

        status = raw.get("status", "due")
        if not isinstance(status, str) or status not in VALID_STATUSES:
            raise ValueError("status must be a known activation status")

        lineage_cite: str | None = None
        if "lineage_cite" in raw:
            raw_lineage_cite = raw["lineage_cite"]
            if not isinstance(raw_lineage_cite, str) or not raw_lineage_cite.strip():
                raise ValueError("lineage_cite must be a non-empty string when present")
            lineage_cite = raw_lineage_cite

        return Relationship(
            relationship_id=relationship_id,
            from_party=text_values["from_party"],
            to_party=text_values["to_party"],
            kind=text_values["kind"],
            next_move=text_values["next_move"],
            due=due,
            why_now=text_values["why_now"],
            status=status,
            lineage_cite=lineage_cite,
        )

    def home(self) -> list[Relationship]:
        """Customer-visible queue: due/rescheduled, earliest due first."""

        rows = [row for row in self._rows.values() if row.status in HOME_STATUSES]
        return sorted(rows, key=lambda row: (row.due, row.relationship_id))

    def get(self, relationship_id: str) -> Relationship:
        """Return one relationship or raise a domain-specific missing-key error."""

        try:
            return self._rows[relationship_id]
        except KeyError as exc:
            raise KeyError(f"unknown relationship {relationship_id}") from exc

    def apply(
        self,
        relationship_id: str,
        action: str,
        *,
        due: str | None = None,
    ) -> Relationship:
        """Apply one allowed move and return the resulting immutable snapshot."""

        if action not in ACTIONS:
            raise ValueError(f"unknown action {action!r}")
        current = self.get(relationship_id)
        if current.status in TERMINAL_STATUSES:
            raise ValueError(
                f"relationship {relationship_id} is terminal ({current.status})"
            )
        if action == "activate":
            updated = Relationship(**{**current.to_dict(), "status": "activated"})
        elif action == "dismiss":
            updated = Relationship(**{**current.to_dict(), "status": "dismissed"})
        else:
            if due is None or due == "":
                raise ValueError("reschedule requires a due date")
            if not isinstance(due, str):
                raise ValueError("due date must be a string")
            date.fromisoformat(due)
            updated = Relationship(
                **{**current.to_dict(), "status": "rescheduled", "due": due}
            )
        self._rows[relationship_id] = updated
        return updated
