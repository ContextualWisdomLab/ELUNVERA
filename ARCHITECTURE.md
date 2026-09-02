# ELUNVERA Architecture

**Status:** Proposed commercialization baseline  
**Updated:** 2026-09-02

## Product responsibility

ELUNVERA owns the operational lifecycle that turns a known relationship into a next move and records the resulting action. It does not own lineage, retrieval, ontology/catalog publication, employment truth, or identity.

## Domain-driven design

### Core subdomain — Relationship Activation

Bounded context: `Relationship Activation`.

- Aggregate root: `RelationshipActivation`
- Entities: durable relationship-local records when persistence lands
- Value objects: `RelationshipReference`, `ActivationMove`, `DueDate`, `WhyNow`, `LineageReference`
- Domain service: transition validation where a rule does not belong to one value object
- Repository: `RelationshipActivationRepository` port; production adapter not yet implemented
- Domain event: immutable `ActivationReceipt`
- Read model: `ActivationQueue`

Transaction invariant: one command modifies at most one relationship activation aggregate and emits at most one idempotent receipt for the command key.

### Supporting subdomain — Interaction and Delivery

Browser/UI and HTTP command/query boundaries. The prototype uses a loopback Python server and static modules. Production delivery must move to an asynchronous/non-blocking boundary and prove realistic k6 p95 <= 20 ms per buyer-facing page before a performance claim.

### Generic/upstream capabilities

Identity is owned by keyverse. Provenance is owned by LineageWeave. Retrieval is owned by RankWeave. Semantic generation/release is owned by ConceptWeave; catalog/governance/search/serve is owned by semantic-data-portal. Employment/organization truth is owned by Orgmetra. Each is reached through a released API/client/schema behind an anti-corruption layer; no source copy or cross-service SQL is allowed.

## Context map

```text
keyverse --------------------> [Identity ACL] -----------+
LineageWeave ----------------> [Provenance ACL] --------+--> Relationship Activation --> Interaction/Delivery
RankWeave (future) ----------> [Retrieval ACL] ---------+
ConceptWeave/SDP (future) ---> [Semantic ACL] ----------+
Orgmetra --------------------> [Organization ACL] ------+
```

Arrows point from upstream authority to ELUNVERA consumption. ELUNVERA domain truth never moves into the upstream products.

## Proposed persistence ERD

No database is implemented on the current PR. The next persistence slice must start with migrations and tests. Proposed 3NF responsibility is:

```text
relationship_record 1 --- * relationship_party
relationship_record 1 --- * activation_move
activation_move      1 --- 0..1 activation_receipt
```

Suggested semantic persistence names intentionally avoid generic one-word objects. Concrete columns/constraints remain Proposed until the migration PR proves them. Tenant identity participates in uniqueness and authorization. `activation_receipt` is immutable; duplicate command delivery is guarded by an explicit idempotency key. Read projections may be separated later only from measured contention/query evidence.

## Current runtime

`src/elunvera/queue.py` implements the in-memory prototype. `scripts/serve.py` exposes it on loopback and starts with zero records. Anonymized test fixtures are injected only in tests. This boundary is deliberately replaceable; it is not a production data source.

## Deployment and operability direction

Production deployment should be compose-based and compatible with Docker/Podman/Colima, preserving a Kubernetes migration path. PostgreSQL/app/shm tuning must be evidence-driven from actual container limits. Backup/restore, migration rollback, health/readiness, structured audit logging, cancellation/resource limits, and security controls must be tested before release.

## UX and internationalization direction

Product UI components should be product-owned reusable components with Storybook normal/loading/empty/error/permission/responsive/interaction scenes. Translation authority must be DB-backed and versioned, with screen-key fetch/cache rather than a full browser catalog. Required locales are ko/en/ja/zh/vi/es/de/fr. Current static prototype has no compliance claim.
