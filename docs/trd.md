# ELUNVERA TRD — first slice

**Date:** 2026-08-27  
**Implements:** [ADR 0001](adr/0001-relationship-activation-home.md), [PRD](prd.md)

## Runtime

- Python 3.12+, stdlib HTTP server (`scripts/serve.py`)
- Static home: `web/`
- Queue logic: `src/elunvera/queue.py`
- Seed: `data/activations.json`
- Tests: `tests/test_queue.py` via pytest

No database, no identity provider, no mail stack.

## Data

Each relationship row:

| Field | Meaning |
| --- | --- |
| `id` | Stable ELUNVERA id (`rel-…`) |
| `from_party` / `to_party` | Display names of the two parties |
| `kind` | `partner` \| `advisor` \| `account-contact` \| `collaborator` — a label, not an SDP term |
| `next_move` | The concrete action |
| `due` | ISO date |
| `why_now` | One-sentence reason the move is due |
| `status` | `due` \| `activated` \| `rescheduled` \| `dismissed` |
| `lineage_cite` | Optional LineageWeave node id. Citation only; never an edge. |

`apply(id, action, due=?)` is the only mutation. There is no graph write path.

## Home

`GET /` serves the activation queue. `GET /api/queue` returns due/rescheduled rows, earliest `due` first. `POST /api/queue/{id}` with `{"action":"activate"|"reschedule"|"dismiss","due":"..."}` mutates the in-memory copy of the seed (process-local).

## CI

`.github/workflows/ci.yml` runs pytest on the exact PR head. Echo-only jobs are not product CI.
