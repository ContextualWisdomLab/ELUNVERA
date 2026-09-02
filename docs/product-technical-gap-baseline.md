# Product / Technical Commercialization Gap Baseline

**Repository:** ContextualWisdomLab/ELUNVERA  
**Evidence date:** 2026-09-02  
**PR:** #1 `product/first-slice-activation-queue`  
**Implementation evidence head:** `b5ceb6ed38e1aa47428a978db4b9a99f358f0c9a` before this documentation reconciliation; re-verify the resulting exact PR head before any merge claim.  
**Product state:** Very early-stage, executable prototype, not production-ready.

## Feature specification

ELUNVERA owns a Relationship Activation bounded context. The current feature surface renders an Activation Queue and accepts Activate, Reschedule, and Dismiss transitions for known relationship records. The customer-facing intent is to make the next move visible, explain why it matters now, and preserve an action receipt. Runtime startup is intentionally empty; production code must not consume synthetic/demo relationship data.

## DDD / context map

Core subdomain: Relationship Activation. Supporting subdomain: Interaction/Delivery. Upstream authorities are keyverse (identity), LineageWeave (provenance), RankWeave (retrieval), ConceptWeave/semantic-data-portal (semantic publication/catalog), and Orgmetra (employment/organization truth). Integrations require released contracts through ACLs; cross-service SQL, copied source, and temp-branch dependencies are prohibited.

Aggregate: `RelationshipActivation`. Value objects: `RelationshipReference`, `ActivationMove`, `DueDate`, `WhyNow`, `LineageReference`. Read projection: `ActivationQueue`. Domain event: immutable `ActivationReceipt`. One command transaction modifies at most one aggregate; durable delivery must be idempotent.

## Proposed persistence ERD

No database is implemented. Proposed 3NF responsibilities, subject to test-first migration evidence:

```text
relationship_record 1 --- * relationship_party
relationship_record 1 --- * activation_move
activation_move      1 --- 0..1 activation_receipt
```

All concrete persistence objects must use semantically specific names. Tenant scoping, uniqueness, immutable receipt constraints, item-level UPSERT/idempotency, lock/contention behavior, migrations, and backup/restore are unresolved.

## Gap register

| Gap | Owner | Current evidence | Action | Status / next verification |
| --- | --- | --- | --- | --- |
| Production data source | ELUNVERA | Prototype runtime is in-memory and now starts empty; bundled synthetic runtime data removed | Define `RelationshipActivationRepository` port, RED tests, 3NF PostgreSQL adapter and real-data ingestion path | **Open** — verify exact-head tests, restart durability, no synthetic runtime path |
| Tenant identity / authorization | keyverse + ELUNVERA ACL | No production identity integration | Read keyverse released PRD/API; implement ACL only against immutable release and enforce tenant authorization | **Open** — fail closed until released contract is available |
| Immutable action receipts / idempotency | ELUNVERA | Prototype mutates process memory only | Persist immutable `activation_receipt`; explicit command idempotency key and item UPSERT tests | **Open** — duplicate delivery/restart tests required |
| Provenance link | LineageWeave + ELUNVERA ACL | Optional `lineage_cite` is only a string | Consume released provenance identifier/receipt contract through ACL; never write lineage edges | **Open** — contract/version/conformance test required |
| Async production web runtime | ELUNVERA | `ThreadingHTTPServer` loopback prototype only | Replace/encapsulate with production non-blocking boundary; preserve domain port | **Open** — realistic E2E evidence required |
| Performance | ELUNVERA | No k6 evidence | Define realistic concurrent workload, profile/fix bottlenecks, record page p95 | **Open** — p95 <=20 ms per buyer-facing page before success claim |
| UX/accessibility | ELUNVERA | Static prototype; no full accessibility evidence | Product-owned reusable components/Storybook; keyboard, focus, screen-reader, responsive, empty/loading/error/permission screenshots/E2E | **Open** |
| Internationalization | ELUNVERA / shared translation owner if released | No DB-backed versioned resource contract | Establish screen-key resource API/cache and ko/en/ja/zh/vi/es/de/fr coverage without shipping full catalog | **Open** |
| Security/compliance | ELUNVERA + .github | Bounded request parsing exists; no product security certification | Exact-head SAST/security/SBOM/provenance, least privilege, PII handling, audit and CSAP/SOC 2 design evidence | **Open** |
| Operability / deployment | ELUNVERA | Local loopback process only | Compose Docker/Podman/Colima path, health/readiness, migrations, backup/restore/rollback and hardware-aware DB config | **Open** |
| Release | ELUNVERA + .github | No immutable product release | Complete gates, CHANGELOG/versioning/provenance, public release after ordinary governance | **Open** |

## Exact-head action completed in this iteration

A test-first regression now requires the default runtime queue to contain no bundled demo relationships, while HTTP tests inject anonymized fixtures. Production startup was changed accordingly and the shipped `data/activations.json` demonstration file was removed. This closes only the **synthetic runtime consumption** sub-gap; it does not close the production-data-source gap because there is not yet a durable real-data adapter.

## Next highest-leverage bounded slice

Implement the repository contract and PostgreSQL persistence test-first: migrations with semantically named 3NF objects, tenant-scoped aggregate key, immutable receipt/idempotency constraints, item-level UPSERT behavior, restart durability, migration rollback and backup/restore evidence. Keep keyverse and other upstream dependencies behind ports until an immutable owner release is available.
