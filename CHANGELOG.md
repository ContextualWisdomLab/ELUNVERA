# Changelog

All notable ELUNVERA changes are recorded here while the product is pre-release.

## Unreleased

### Changed

- Reconciled the first-slice PRD/TRD/ADR with its actual prototype maturity and DDD/product boundaries.
- Runtime startup now contains no fabricated relationships; anonymized synthetic data is test-only.
- Added architecture and commercialization-gap baselines so production persistence, identity, operability, UX, security, performance, and ecosystem work have explicit owners and verification criteria.
- Retargeted the first-slice PR to the canonical `main` release branch after verifying `main` and `develop` shared the same base revision.
- Replaced the misleading empty-queue success message with an actionable no-relationship state and live-region semantics.
- Removed internal repository/product implementation names from buyer-facing page copy.
- Replaced generic `id` relationship fields with semantic `relationship_id` identifiers across the prototype and browser action boundary.
- Renumbered the Proposed relationship-activation decision to ADR `0017` so it can follow the foundation branch's `0001`–`0016` ADR range without collision; references were migrated before the old path was retired.
- Made product CI review every pull-request base (including verified stacked prerequisites), limited push CI to canonical `main`, and added exact-head checkout verification so stack validation does not depend on a stale branch allowlist.

### Security and reliability

- Preserved bounded request-body validation and fail-closed action validation from the existing review repairs.
- Kept production data separate from bundled test fixtures to prevent demo records from being mistaken for customer state.
- Replaced generic repository-root static serving with an explicit allowlist for the product HTML/CSS/JavaScript surface; repository docs, workflows, dependency manifests, and other internal files now return 404 from the prototype HTTP boundary.
- Added test-first aggregate identity guards: relationship identifiers must be non-empty strings and duplicate `relationship_id` snapshots are rejected instead of silently overwriting an existing aggregate.
- Added test-first source-snapshot validation for real ISO due dates and known activation statuses, and made activated/dismissed relationships terminal so repeated commands fail closed instead of rewriting a completed decision.
