# ELUNVERA

> **Every Link, Understood. Every Relationship, Activated.**

ELUNVERA is ContextualWisdomLab's relationship-activation product. It keeps the next move on a known relationship visible and actionable.

The current branch is an executable **prototype**, not a production CRM service. Runtime startup is intentionally empty: production code never loads bundled synthetic customer or relationship records. Tests inject anonymized fixtures explicitly.

This repository uses GitHub flow: product pull requests target `main` and squash-merge after exact-head checks and qualifying review. `develop` is not a release authority.

## Product boundary

| Product | Owns | ELUNVERA does not |
| --- | --- | --- |
| LineageWeave | lineage/provenance DAG | invent a second lineage graph |
| RankWeave | retrieval fusion/evaluation | rank or search corpora |
| ConceptWeave / semantic-data-portal | semantic generation/release and catalog governance | become an ontology/catalog authority |
| Orgmetra | employment/organization truth | store jobs, org charts, or employment records |
| keyverse | identity/federation/token contracts | invent another identity authority |

ELUNVERA owns relationship activation: a known relationship, its next move, why the move is due, and the action receipt. Neighbor integrations must use released contracts through ACLs; ELUNVERA must not copy source or query another product's database.

See [ADR 0001](docs/adr/0001-relationship-activation-home.md), [PRD](docs/prd.md), [TRD](docs/trd.md), [ARCHITECTURE](ARCHITECTURE.md), and the [commercialization gap baseline](docs/product-technical-gap-baseline.md).

## Run the prototype surface

```bash
python3 scripts/serve.py
```

Open http://127.0.0.1:8765/. An empty queue is the correct startup state until a real-data repository adapter is implemented.

```bash
python3 -m pytest -q
```
