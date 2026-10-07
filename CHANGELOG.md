# Changelog

All notable changes to ELUNVERA will be documented in this file.

The format follows Keep a Changelog principles, and versioning will begin when the first executable release candidate exists.

## [Unreleased]

### Added

- A pinned Rust 1.97.1 workspace seed with a fail-closed `domain_contracts` version boundary and exact CI gates for format, Clippy, tests, documentation, and complete line/function/region/branch coverage.
- The first executable relationship-activation prototype: an in-memory queue, loopback-only HTTP boundary, static browser surface, and anonymized Python/browser tests with complete owned-code coverage.
- Proposed ADR-0017 for the Activation Queue aggregate, command transitions, immutable receipt direction, and ecosystem anti-corruption boundaries.
- Initial ELUNVERA product and technical documentation baseline.
- Product requirements, technical requirements, architecture, data model, API and event contracts.
- Security, privacy, threat-model, testing, operability, UX, user-story, use-case, storyboard, wireframe, and Storybook baselines.
- Architecture decision record set covering product ownership, modularity, identity, tenancy, temporal facts, relationships, integrations, privacy, AI, persistence, APIs, quality, UX, retention, and ecosystem boundaries.
- OpenAPI 3.2.0 and AsyncAPI 3.1.0 draft contracts.
- Initial product-technical gap baseline and phased implementation plan.
- Public documentation landing and exact-cased DeepWiki entry point.
- Apache License 2.0 grant for ContextualWisdomLab-authored ELUNVERA source and documentation, with trademark and third-party rights kept separate.
- Proposed eight-locale (`ko/en/ja/zh/vi/es/de/fr`) product contract with DB-backed versioned translation-resource authority, review/approval/deploy/rollback semantics, screen-key-scoped delivery, and separation from ontology labels.
- Proposed realistic k6 every-buyer-page p95 ≤ 20 ms release contract, with full measured denominator and causal profiling requirements.

### Fixed

- Serialized prototype activation transitions with a snapshot-identity compare-and-set so concurrent and ABA-stale commands cannot overwrite an accepted decision.
- Preserved accepted-command truth across ambiguous transport rejection, unreadable success responses, and later queue-refresh failures, disabled unsafe stale retries, and added anti-framing response headers for the loopback UI.
- Integrated the complete product/technical foundation into the executable prototype stack without discarding either valid delta, and made uppercase `docs/PRD.md`, `docs/TRD.md`, and `docs/ARCHITECTURE.md` the single canonical authorities.
- Reconciled the first-slice PRD/TRD/ADR with its actual prototype maturity and DDD/product boundaries.
- Runtime startup now contains no fabricated relationships; anonymized synthetic data is test-only.
- Retargeted the first-slice PR to canonical `main` after verifying that `main` and `develop` shared the same base revision.
- Replaced the misleading empty-queue success message with an actionable no-relationship state and live-region semantics.
- Removed internal repository/product implementation names from buyer-facing page copy.
- Replaced generic `id` relationship fields with semantic `relationship_id` identifiers across the prototype and browser action boundary.
- Decoded browser-encoded relationship identifiers at the HTTP boundary so valid identifiers containing spaces, slashes, or non-ASCII characters round-trip to queue commands.
- Renumbered the Proposed relationship-activation decision to ADR `0017` so it follows the foundation ADR range without collision.
- Made product CI review every pull-request base, limited push CI to canonical `main`, and added exact-head checkout verification.
- Restricted the P0 manual relationship command to manual truth states and required non-empty evidence or a non-blank manual assertion reason.
- Made the permanent document-contract gate reject trailing whitespace in committed tracked text and cleaned the affected product-technical gap baseline.
- Aligned the narrative HTTP inventory with the authoritative OpenAPI P0 surface.
- Added temporal read parameters and effective-lens response headers to the machine-readable HTTP contract.
- Corrected AsyncAPI operations to publish ELUNVERA domain events and required classification/schema metadata.
- Added explicit `recorded_at` payload fields so outbox publication delay cannot corrupt bitemporal reconstruction.
- Removed one-shot reconciliation/review-repair workflows and script from the publishable candidate before final manifest sealing.
- Retargeted the Draft foundation to canonical protected `main`, aligned document-contract and review automation with that base, and corrected stale `develop` navigation/governance claims.
- Returned ADR-0013 to `Proposed` while the foundation remains unmerged; protected integration is required before the decision may be marked `Accepted`.
- Aligned AGENTS, contributing guidance, PRD, roadmap, and implementation plan/spec branch authority with canonical protected `main`; stacked work may target only its verified prerequisite branch, and document-contract CI now guards that authority against drift.
- Replaced the earlier 300–1500 ms page targets and two-locale release assumptions with the current commercialization contract; document-contract CI now fails closed if PRD/TRD/UX/Test Strategy regress from the p95 ≤ 20 ms and eight-locale requirements.
- Added DDD ownership and persistence expectations for `translation_resource`, `translation_revision`, and `translation_text`, including immutable approved revisions and explicit draft item-level UPSERT semantics.

### Security

- Kept production data separate from bundled test fixtures and retained bounded request-body/action validation.
- Replaced repository-root static serving with an explicit product-asset allowlist; repository docs, workflows, and dependency manifests return 404.
- Added test-first guards for non-empty semantic relationship identity, duplicate snapshots, real ISO due dates, known statuses, terminal activated/dismissed states, non-empty buyer-visible facts, typed optional provenance, and non-string HTTP actions.
- Defined fail-closed tenant isolation, purpose-aware authorization, immutable audit, model provenance, controlled egress, and customer-data disclosure boundaries.
- Required model-backed GitHub Actions to consume the released contextual-orchestrator gateway through `orchestrator/free` only, with no workflow-selected provider/model/paid fallback.

### Notes

- The executable runtime is a Draft loopback prototype, not a production service. No database schema, deployment artifact, customer performance measurement, eight-locale implementation, protected-main integration, or release exists. The broader contracts remain requirements, not evidence of conformance.
