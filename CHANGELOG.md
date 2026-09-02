# Changelog

All notable ELUNVERA changes are recorded here while the product is pre-release.

## Unreleased

### Changed

- Reconciled the first-slice PRD/TRD/ADR with its actual prototype maturity and DDD/product boundaries.
- Runtime startup now contains no fabricated relationships; anonymized synthetic data is test-only.
- Added architecture and commercialization-gap baselines so production persistence, identity, operability, UX, security, performance, and ecosystem work have explicit owners and verification criteria.

### Security and reliability

- Preserved bounded request-body validation and fail-closed action validation from the existing review repairs.
- Kept production data separate from bundled test fixtures to prevent demo records from being mistaken for customer state.
