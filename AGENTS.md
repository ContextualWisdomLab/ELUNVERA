# ELUNVERA Agent Guide

## Product authority

ELUNVERA owns relationship activation: the known relationship reference, next move, why-now evidence, allowed transition, and immutable action receipt. Preserve exact product/repository capitalization.

Do not copy or query internal storage from LineageWeave, RankWeave, ConceptWeave, semantic-data-portal, Orgmetra, or keyverse. Consume only immutable released contracts through explicit ACLs; use ports/test doubles until a supplier release exists.

## Development invariants

- Work test-first for behavior changes and preserve concurrent writer commits; never force-push or destructively rebase.
- Keep PRD/TRD/ADR/ARCHITECTURE/CHANGELOG and `docs/product-technical-gap-baseline.md` aligned with the exact implementation evidence.
- Runtime must not consume synthetic demonstration data. Test fixtures must be anonymized.
- Keep one command transaction scoped to one relationship-activation aggregate. Durable mutations require explicit idempotency/UPSERT contracts and immutable receipts.
- PostgreSQL objects use semantically specific names with at least two words and 3NF by default.
- Do not claim identity, persistence, accessibility, performance, security, internationalization, backup/restore, or release maturity without exact-head evidence.
- Product UI hides internal repository/service boundaries and guides the customer to the next action.
- Production web handling must be asynchronous/non-blocking and realistic k6 page p95 must be <=20 ms before claiming the target is met.

## Current maturity

The first PR is an executable loopback prototype. It starts empty and uses anonymized test fixtures. Production identity, durable persistence, released upstream integrations, deployment, accessibility/i18n, load evidence, and release engineering remain gaps.
