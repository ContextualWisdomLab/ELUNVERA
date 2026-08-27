# AGENTS.md — ELUNVERA

## Required reading order

Before changing this repository, read:

1. `README.md`
2. `docs/PRD.md`
3. `docs/TRD.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DATA_MODEL.md`
6. `docs/product-technical-gap-baseline.md`
7. `docs/adr/README.md`
8. the relevant ADRs and doctoring material
9. the current pull request, exact head, checks, reviews, and unresolved threads

The repository and current GitHub state are the source of truth. Private memory and prior chat summaries are not.

## Product responsibility

ELUNVERA is the authoritative system for tenant-scoped customer relationship and commercial opportunity facts. It must not absorb capabilities owned by another ContextualWisdomLab product.

Never turn ELUNVERA into:

- an email or calendar host;
- an ERP, CPQ, accounting, payment, or subscription ledger;
- an HRIS;
- a generic issue tracker or project manager;
- an ontology catalog;
- an autonomous agent that changes customer or opportunity facts without policy and human authority.

## Data and naming rules

- Database objects use `snake_case` and at least two words.
- Every tenant-owned row has an enforced tenant boundary.
- Temporal facts preserve business-valid time and system-recorded time.
- Relationships are first-class facts with evidence, provenance, confidence, and validity.
- External IDs are references, never internal primary keys.
- Provider payloads do not define canonical domain state.
- Raw PII is not broadcast through events or model traces.
- Ingestion uses item-level idempotency and records an immutable receipt.
- Hard delete is forbidden for audit, stage history, relationship history, model evidence, and legal-hold material.

## Engineering rules

- Use Rust for the API, domain services, high-throughput ingestion, security-sensitive logic, graph computations, vector operations, statistics, and model calculations.
- TypeScript may implement the web interface and generated clients.
- Python is permitted for non-production validation, research comparison, or connector glue only when no production numerical logic is introduced.
- Do not suppress deprecation warnings. Fix the cause.
- Do not introduce arbitrary weights, hard-coded “health scores,” stage-derived probabilities, or rule-of-thumb forecasts.
- All AI results are proposals or evidence-linked assessments until an authorized workflow accepts them.
- Do not send customer source content directly to a model provider outside `contextual-orchestrator` contracts.
- Do not mix unrelated dependency or refactoring changes into a product slice.

## Test and documentation gates

For ELUNVERA-owned production code:

- statement coverage: 100%;
- branch coverage: 100%;
- public module/type/trait/function/method documentation: 100%;
- property and fuzz tests for parser, identifier, temporal, money, and authorization boundaries;
- real PostgreSQL integration tests;
- tenant-isolation and purpose-authorization tests;
- migration clean-install, upgrade, rollback, and restoration rehearsals;
- CPU/GPU parity and true-parameter recovery for any numerical model;
- no skipped or ignored required GPU lane;
- accessibility, keyboard, responsive, print/export, and internationalization tests for user interfaces.

Update `CHANGELOG.md`, `docs/product-technical-gap-baseline.md`, affected ADRs, contracts, and doctoring traceability in the same pull request.

## Pull request operation

Use `develop` as the base branch unless an explicitly approved stack requires another feature branch.

Before commit or push:

1. re-read remote branch and pull-request state;
2. preserve concurrent agent changes and understand their intent;
3. remove one-shot or self-modifying workflows after their bounded purpose;
4. run the exact validation commands claimed in the pull request;
5. record actual evidence, not anticipated results.

Never claim a check passed if it is queued, pending, skipped, or was run on an older head. Never force-push over another agent’s work merely because the branch changed.
