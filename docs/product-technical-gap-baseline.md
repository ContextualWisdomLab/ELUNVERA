# Product / Technical Commercialization Gap Baseline

**Repository:** ContextualWisdomLab/ELUNVERA  
**Evidence date:** 2026-09-02  
**PR:** #1 `product/first-slice-activation-queue` targeting canonical `main`  
**Implementation evidence:** current writer branch; re-fetch the resulting exact PR head and exact-head Checks before any merge claim.  
**Product state:** Very early-stage, executable prototype, not production-ready.

## Feature specification

ELUNVERA owns a Relationship Activation bounded context. The current feature surface renders an Activation Queue and accepts Activate, Reschedule, and Dismiss transitions for known relationship records. The customer-facing intent is to make the next move visible, explain why it matters now, and preserve an action receipt. Runtime startup is intentionally empty; production code does not consume bundled synthetic/demo relationship data.

The current browser surface distinguishes “no relationships available” from “all work completed,” exposes status/empty changes through polite status live regions, keeps buyer copy free of internal repository boundaries, and serves only the explicitly required product HTML/CSS/JavaScript paths. Repository documentation, workflow files, dependency manifests, and arbitrary repository-root paths are not exposed through the prototype HTTP server.

Relationship identity is now explicit at the prototype boundary: `relationship_id` is a semantic aggregate identifier, non-string/blank identifiers fail closed, and duplicate snapshots with the same identifier are rejected instead of silently overwriting an existing aggregate. This is an in-memory invariant only; durable tenant-scoped uniqueness and idempotency remain unimplemented.

## DDD / context map

Core subdomain: Relationship Activation. Supporting subdomain: Interaction/Delivery. Upstream authorities are keyverse (identity), LineageWeave (provenance), RankWeave (retrieval), ConceptWeave/semantic-data-portal (semantic publication/catalog), and Orgmetra (employment/organization truth). Integrations require released contracts through ACLs; cross-service SQL, copied source, and temp-branch dependencies are prohibited.

Aggregate: `RelationshipActivation`. Value objects: `RelationshipReference`, `ActivationMove`, `DueDate`, `WhyNow`, `LineageReference`. Read projection: `ActivationQueue`. Domain event: immutable `ActivationReceipt`. One command transaction modifies at most one aggregate; durable delivery must be idempotent. The aggregate identity invariant is one unique non-empty `relationship_id` per snapshot set; duplicate identity input must fail closed until a repository-level UPSERT contract is intentionally defined.

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
| Product authority / foundation integration | ELUNVERA | PR #2 carries the broader PRD/TRD/API/data/security/UX foundation and was retargeted to protected `main`; PR #1 independently carries lowercase PRD/TRD plus ADR `0001`, creating duplicate authority and ADR-number collision if naively combined | Preserve both valid deltas; make PR #2 the foundation prerequisite, then non-destructively reconcile PR #1 into the canonical docs, renumber the activation ADR after the foundation ADR range, and revalidate exact-head contracts | **Open** — no merge until one canonical authority remains and all runtime deltas are preserved |
| Production data source | ELUNVERA | Prototype runtime is in-memory and starts empty; bundled synthetic runtime data removed | Define `RelationshipActivationRepository` port, RED tests, 3NF PostgreSQL adapter and real-data ingestion path | **Open** — exact-head tests, restart durability, no synthetic runtime path |
| Tenant identity / authorization | keyverse + ELUNVERA ACL | No production identity integration | Read keyverse released PRD/API; implement ACL only against immutable release and enforce tenant authorization | **Open** — fail closed until released contract is available |
| Aggregate identity | ELUNVERA | Test-first guards require semantic non-empty `relationship_id` and reject duplicate in-memory snapshots | Carry uniqueness into tenant-scoped repository schema and explicit item-level UPSERT semantics without silent overwrite | **Partially mitigated** — durable uniqueness/concurrency tests required |
| Immutable action receipts / idempotency | ELUNVERA | Prototype mutates process memory only | Persist immutable `activation_receipt`; explicit command idempotency key and item UPSERT tests | **Open** — duplicate delivery/restart tests required |
| Provenance link | LineageWeave + ELUNVERA ACL | Optional `lineage_cite` is only a string | Consume released provenance identifier/receipt contract through ACL; never write lineage edges | **Open** — contract/version/conformance test required |
| HTTP exposure boundary | ELUNVERA | Test-first allowlist serves only index + required CSS/JS + queue API; internal repo files return 404 | Keep route allowlist regression coverage as runtime changes | **Mitigated in prototype** — exact-head CI/security scan still required |
| Buyer-facing empty/action copy | ELUNVERA | Empty state is truthful/actionable, uses polite status semantics; internal repo names removed | Browser/E2E audit focus, focus-not-obscured, screen reader, responsive and error scenes | **Partially mitigated** — no accessibility conformance claim |
| Async production web runtime | ELUNVERA | `ThreadingHTTPServer` loopback prototype only | Replace/encapsulate with production non-blocking boundary; preserve domain port | **Open** — realistic E2E evidence required |
| Performance | ELUNVERA | No k6 evidence | Define realistic concurrent workload, profile/fix bottlenecks, record page p95 | **Open** — p95 <=20 ms per buyer-facing page before success claim |
| UX/accessibility | ELUNVERA | Static prototype; live-region/empty-state regression exists but no full audit | Product-owned reusable components/Storybook; keyboard, focus, screen-reader, responsive, empty/loading/error/permission screenshots/E2E | **Open** |
| Internationalization | ELUNVERA / shared translation owner if released | No DB-backed versioned resource contract | Establish screen-key resource API/cache and ko/en/ja/zh/vi/es/de/fr coverage without shipping full catalog | **Open** |
| Security/compliance | ELUNVERA + .github | Bounded request parsing and route allowlist exist; no product certification | Exact-head SAST/security/SBOM/provenance, least privilege, PII handling, audit and CSAP/SOC 2 design evidence | **Open** |
| Operability / deployment | ELUNVERA | Local loopback process only | Compose Docker/Podman/Colima path, health/readiness, migrations, backup/restore/rollback and hardware-aware DB config | **Open** |
| Release | ELUNVERA + .github | No immutable product release | Complete gates, CHANGELOG/versioning/provenance, public release after ordinary governance | **Open** |

## Evidence-backed actions completed in this iteration

The runtime-synthetic-data sub-gap was repaired test-first: `test_default_runtime_queue_starts_empty` was committed before the runtime change, HTTP tests inject anonymized fixtures, and the shipped demonstration-data file was deleted. The customer empty state was then repaired test-first so zero records no longer imply that every due relationship was completed. Buyer-facing copy is guarded against leaking internal product/repository names, and an HTTP-boundary regression preceded the explicit product-asset allowlist.

The aggregate-identity sub-gap was also repaired test-first on the canonical PR #1 writer branch. RED coverage first established that duplicate `relationship_id` snapshots and non-string/blank identities must fail closed; the production queue now enforces those invariants. This prevents silent aggregate replacement in the prototype but does not claim persistent uniqueness, multi-tenant correctness, idempotent delivery, or restart durability.

Live repository evidence also establishes a prerequisite integration gap: PR #2 is the broader documentation/contract foundation and now targets canonical protected `main`, while PR #1 contains independent lowercase PRD/TRD documents and a conflicting ADR `0001`. These deltas must be reconciled by dependency order rather than closing either PR or accepting two product authorities.

These changes do **not** close the production-data-source, accessibility, security, production-runtime, persistence, or foundation-integration gaps. Exact-head workflow results and qualifying independent review remain required after the final documentation commit.

## Next highest-leverage bounded slice

First reconcile the foundation/runtime dependency without losing either PR’s valid delta: get PR #2’s canonical-main document contract evidence current, then integrate PR #1 atop that authority, renumber its activation ADR after the foundation ADR range, and collapse duplicate PRD/TRD authority into the canonical documents. After that, implement the durable repository contract without extending the prototype into an accidental Python production monolith. Start RED tests for tenant-scoped repository semantics, immutable receipt/idempotency and restart durability; then select the production PostgreSQL/runtime boundary consistent with the Rust-default performance/security policy. Persistence must use semantically named 3NF objects, explicit item UPSERT behavior, migration rollback and backup/restore evidence. Keep keyverse and other upstream dependencies behind ports until immutable owner releases are available.
