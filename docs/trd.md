# ELUNVERA TRD — relationship activation

**Updated:** 2026-09-02  
**Implements:** [ADR 0001](adr/0001-relationship-activation-home.md), [PRD](prd.md)

## Current executable slice

- Python 3.12+ prototype HTTP boundary: `scripts/serve.py`
- Static browser surface: `web/`
- Queue domain prototype: `src/elunvera/queue.py`
- Python and browser tests: `tests/`
- Exact-head product CI: `.github/workflows/ci.yml`

Runtime starts with an empty `ActivationQueue`. Production code does not load bundled demonstration records. Tests inject anonymized fixtures explicitly.

The loopback HTTP prototype exposes only `/`, `/index.html`, `/api/queue`, the queue command path, and an explicit allowlist of required browser assets (`/web/styles.css`, `/web/bootstrap.js`, `/web/app.js`). It does not delegate arbitrary GET paths to repository-root static serving. Repository docs, workflows and dependency manifests therefore remain outside the customer HTTP surface.

## Domain contract

A relationship snapshot currently exposes `id`, `from_party`, `to_party`, `kind`, `next_move`, `due`, `why_now`, `status`, and optional `lineage_cite`. `apply(relationship_id, action, due=?)` is the only mutation in the prototype. There is no graph write path.

The current in-memory implementation is a replaceable adapter, not the durable repository contract.

## Proposed persistence boundary

The next production persistence slice must use PostgreSQL in 3NF with semantically named objects. Proposed tables are `relationship_record`, `relationship_party`, `activation_move`, and immutable `activation_receipt`; concrete columns, keys and transaction boundaries remain Proposed until test-first migration work lands. One-word generic persistence-object names are prohibited. Item-level UPSERT/idempotency must be explicit and tested. Tenant ownership belongs in the aggregate key and authorization boundary, not in process-global state.

Write transactions should be minimal: one relationship activation aggregate per command. Cross-product references such as LineageWeave provenance are identifiers received through released APIs/ACLs, never foreign database joins.

## Security and operability direction

The current server binds only to loopback, uses a fail-closed route allowlist, and is not a production deployment. Production work must add keyverse-backed authentication, least-privilege database credentials, migration/backup/restore evidence, structured audit receipts, cancellation/resource bounds, compose-based deployment, and security evidence aligned with CSAP/SOC 2 goals.

## Web validation direction

Production HTTP work must be asynchronous/non-blocking and measured with realistic k6 end-to-end load; each buyer-facing page targets p95 <= 20 ms. UX verification must cover empty/loading/error/permission states, keyboard and screen-reader behavior, responsive layouts, and ko/en/ja/zh/vi/es/de/fr resource boundaries before claims of accessibility or international readiness. The current polite live-region and truthful empty-state behavior is only partial prototype evidence.

## CI

`.github/workflows/ci.yml` runs Python tests with complete touched-production statement/branch coverage, compiles Python entry points, and runs browser tests with complete line/branch/function coverage. Security/review evidence outside this local product workflow must still be exact-head and qualifying before merge.
