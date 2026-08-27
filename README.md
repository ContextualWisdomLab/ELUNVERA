# ELUNVERA

> **Every Link, Understood. Every Relationship, Activated.**

ELUNVERA is ContextualWisdomLab's **relationship-activation** product. It keeps the next move on a known relationship visible and actionable.

This repository uses GitHub flow: pull requests target `main` and squash-merge. `develop` exists as a matching ref today; it is not the merge base for this product home.

## Boundary

ELUNVERA does **not** own these neighboring products. It consumes them later; it does not copy them.

| Product | Owns | ELUNVERA does not |
| --- | --- | --- |
| LineageWeave | Lineage DAG / provenance | Invent a second relationship graph |
| RankWeave | Retrieval fusion | Rank or search corpora |
| Ontology / SDP | Catalog of types and terms | Own the type catalog |
| Orgmetra | Employment truth | Store jobs, org charts, or employment records |

ELUNVERA also does not absorb naruon mail chrome or GNB calendar/mail surfaces.

See [ADR 0001](docs/adr/0001-relationship-activation-home.md), [PRD](docs/prd.md), and [TRD](docs/trd.md).

## Run the first surface

```bash
python3 scripts/serve.py
```

Open http://127.0.0.1:8765/ — the activation queue is the home. No graph. No inbox.

```bash
python3 -m pytest -q
```
