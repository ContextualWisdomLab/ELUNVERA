# ADR 0001: ELUNVERA is the relationship-activation home

- **Status:** Proposed
- **Date:** 2026-08-27
- **Scope:** ContextualWisdomLab/ELUNVERA first slice (this repository only)

## Context

CWL already has products that know *structure*, *search*, *types*, and *employment*. None of them keep a relationship *in motion*: the next concrete move, why it is due now, and the receipt that the move happened.

The 27 Aug 2026 tagline is the product contract: **Every Link, Understood. Every Relationship, Activated.**

## Decision

ELUNVERA is the relationship-activation product. The first customer-visible surface is an **activation queue**: each row is one known relationship plus its next move. Completing, rescheduling, or dismissing that move is the product verb.

This repository is independently runnable. Later hosts may embed the queue; they do not redefine it.

### Neighbor contrast (do not duplicate)

| Neighbor | Authority | What ELUNVERA must not become |
| --- | --- | --- |
| **LineageWeave** | Lineage DAG — how things descend, derive, and provenance-link | A second relationship graph, DAG canvas, or edge store. ELUNVERA may later *cite* a LineageWeave node id; it must not invent lineage edges. |
| **RankWeave** | Retrieval fusion — how results are fused and ranked | A search box, corpus ranker, or fusion layer. The queue is already-known links, not retrieval. |
| **Ontology / SDP** | Catalog — types, terms, and shared meaning | A type catalog, schema registry, or ontology editor. Relationship *kind* on a queue row is a label, not catalog authority. |
| **Orgmetra** | Employment truth — jobs, posts, and who holds them | An org chart, job analysis, or employment record. A collaborator on the queue is not an Orgmetra post. |

### Also out of scope for this slice

- naruon mail chrome, threads, or compose
- GNB calendar, board, or customer-master copies
- A second CWL identity, billing, or ledger surface

## Consequences

- Home is the queue, not a graph, inbox, or search.
- Persistence is ELUNVERA-local for this slice (JSON file). Foreign keys to neighbors are optional citations, never required.
- Merge path is squash onto `main`. This ADR does not open work in LineageWeave, RankWeave, Ontology/SDP, or Orgmetra.
