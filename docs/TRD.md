# ELUNVERA Technical Requirements Document

- **Document version:** 0.1
- **Status:** Proposed technical baseline
- **Date:** 2026-08-27

## 1. Technical objective

Build a Rust-first, tenant-isolated, evidence-centered CRM that preserves relationship and commercial history, integrates with CWL products through versioned contracts, and supports deterministic operation without requiring an LLM or external SaaS provider for core transaction paths.

## 2. Architectural style

ELUNVERA begins as a **modular monolith with independently testable modules**, one PostgreSQL system of record, durable background workers, and a transactional outbox. Clear domain ports permit later extraction only when workload, release cadence, regulatory boundary, or independent ownership justifies a service split.

A microservice-per-noun design is explicitly rejected. It would create distributed transactions before domain boundaries and workloads are proven.

## 3. Technology baseline

| Layer | Baseline | Requirement |
|---|---|---|
| Backend | Rust | Stable compiler pinned in repository; async, multithreaded runtime |
| HTTP | Axum or an equivalent reviewed Rust framework | OpenAPI-generated/validated contract and structured errors |
| Database | PostgreSQL 18.6+ within supported 18.x | RLS, temporal constraints, UUIDv7, partitioning, logical backup/restore |
| Web | React/Next.js TypeScript | Server-rendered where appropriate; accessible progressive enhancement |
| Contracts | OpenAPI 3.2.0, AsyncAPI 3.1.0, JSON Schema 2020-12 | Generated clients and conformance fixtures |
| Events | CloudEvents 1.0 envelope | At-least-once delivery and consumer idempotency |
| Identity | Keyverse OIDC/OAuth 2.1 and SCIM | No local password authority |
| Telemetry | OpenTelemetry | No raw customer content or high-cardinality PII attributes |
| Packaging | OCI images and generated SDK packages | Digest-pinned dependencies, SBOM, provenance, signatures |
| Local runtime | Compose-compatible Podman/Colima/Docker | K8s portability without requiring K8s for development |

Exact dependency versions are selected and lock-pinned in implementation PRs. “Latest” is not a reproducible dependency specification.

## 4. Repository target structure

```text
ELUNVERA/
├── apps/
│   ├── elunvera_api/
│   ├── elunvera_worker/
│   ├── elunvera_web/
│   └── elunvera_admin/
├── crates/
│   ├── domain_contracts/
│   ├── authorization_context/
│   ├── account_registry/
│   ├── party_registry/
│   ├── relationship_registry/
│   ├── interaction_timeline/
│   ├── commitment_registry/
│   ├── opportunity_management/
│   ├── customer_outcomes/
│   ├── complaint_management/
│   ├── privacy_rights/
│   ├── audit_provenance/
│   ├── integration_outbox/
│   ├── search_projection/
│   └── model_evidence/
├── integrations/
│   └── cwl/
│       ├── keyverse_adapter/
│       ├── naruon_adapter/
│       ├── contextual_orchestrator_adapter/
│       ├── semantic_data_portal_adapter/
│       ├── scopeweave_adapter/
│       └── billing_control_plane_adapter/
├── packages/
│   ├── typescript_sdk/
│   └── design_tokens/
├── database/
│   ├── migrations/
│   └── fixtures/
├── schemas/
├── tests/
│   ├── contract/
│   ├── integration/
│   ├── property/
│   ├── fuzz/
│   ├── security/
│   ├── performance/
│   └── e2e/
├── docs/
└── infrastructure/
```

This is a target layout, not a statement that these components exist.

## 5. Domain modules

### 5.1 Authorization context

Consumes a verified Keyverse token and produces an immutable request context:

```text
actor_reference
tenant_reference
workspace_reference
role_set
purpose_code
decision_reference
correlation_id
authentication_strength
token_issued_at
token_expires_at
```

No domain function accepts a caller-supplied tenant ID as authority. The verified context supplies tenant scope.

### 5.2 Account registry

Owns commercial account identity, lifecycle, hierarchy references, role assignments, duplicate review, merge/split receipts, and current account projection.

### 5.3 Party registry

Owns tenant-scoped party records for persons, organizations, and groups, plus names, identifiers, contact points, and source mappings. It must preserve local identity without asserting that different tenants refer to the same real-world party.

### 5.4 Relationship registry

Owns first-class, time-valid party and account relations. It distinguishes authoritative, observed, inferred, proposed, rejected, and superseded facts.

### 5.5 Interaction timeline

Owns manual interactions and normalized metadata projections. Raw external messages remain with the source provider or customer-controlled system.

### 5.6 Commitment registry

Owns relationship commitments and their state transitions. General project execution may be delegated to ScopeWeave through an external work reference.

### 5.7 Opportunity management

Owns opportunity facts, sales-process versions, stages, transitions, stakeholders, values, forecast snapshots, assumptions, products/offerings by reference, and outcome linkage.

### 5.8 Customer outcomes and complaints

Owns desired outcomes, observations, complaint lifecycle, remedies, satisfaction measurement references, and released relationship assessments.

### 5.9 Privacy rights

Owns purpose registry, communication preferences, consent or other processing-basis references, data-rights cases, retention decisions, legal hold, disposition receipts, and export manifests.

### 5.10 Audit and provenance

Owns immutable audit events, source receipts, model claims, evidence links, event publication receipts, and data-transformation lineage.

## 6. Persistence requirements

### 6.1 Canonical relational store

- PostgreSQL is the authoritative store.
- Canonical domain data is normalized to 3NF.
- JSONB is restricted to immutable provider payload metadata, schema-versioned extension values, or diagnostic context that does not determine money, authorization, tenancy, stage, relationship truth, or model score.
- Graph, search, vector, analytics, and dashboard stores are rebuildable projections.
- External system identifiers are isolated in mapping tables.

### 6.2 Identifiers

- Use UUIDv7 for externally visible aggregate identifiers.
- Never expose sequential database identifiers.
- Do not infer creation time for authorization or business logic from UUID ordering.
- Source event identity is `(source_authority, source_event_key)`.

### 6.3 Bitemporal facts

Time-valid facts carry:

```text
valid_time        tstzrange
recorded_time     tstzrange
```

PostgreSQL 18 temporal constraints or equivalent exclusion constraints prevent overlapping active intervals where the domain requires uniqueness.

`valid_time` means when the fact was true in the business domain. `recorded_time` means when ELUNVERA believed or stored that version.

### 6.4 Monetary values

- Store money as exact decimal numeric plus currency code.
- Store quantity, unit, rate, and amount separately.
- Preserve every value and forecast snapshot; corrections append reversal/replacement facts.
- Never use `f32` or `f64` for monetary calculations.

### 6.5 Partition and hot-key policy

Partition only with measured evidence. The release benchmark shall evaluate:

- hash partitioning by tenant for high-volume audit and interaction tables;
- range subpartitioning by recorded month;
- isolation of very large tenants;
- index locality for account timelines;
- queue and outbox contention;
- vacuum and retention behavior.

A tenant ID alone must not create a single unbounded hot partition.

## 7. Transaction requirements

- Aggregate state and its outbox event commit in the same database transaction.
- Optimistic concurrency uses explicit version or ETag.
- Commands require an idempotency key.
- A successful response includes an operation receipt and resulting aggregate version.
- Retries with the same key and payload return the same result.
- Reuse of a key with a different payload fails closed.
- Every ingestion batch has item-level results; one malformed item does not silently discard neighboring items.

## 8. HTTP requirements

- Base path: `/v1`.
- Content type: JSON unless an explicit export/import media type is defined.
- Errors: RFC 9457 Problem Details.
- Pagination: opaque cursor, deterministic order, bounded page size.
- Conditional writes: ETag and `If-Match` for user-editable aggregates.
- Request body and upload limits enforced before full allocation.
- Long operations return `202 Accepted` and a durable job reference.
- Cancellation is explicit and records whether work was never started, cancelled, or completed before cancellation.

## 9. Event requirements

Every domain event uses a CloudEvents envelope and includes:

```text
specversion
id
source
type
subject
time
datacontenttype
tenantref
correlationid
causationid
provenanceref
purposecode
dataclassification
schemarevision
```

The internal metadata names `data_classification` and `schema_revision` serialize as the wire attributes `dataclassification` and `schemarevision`. `time` is publication time. Event payloads that describe bitemporal facts also require an immutable `recorded_at`; consumers must not substitute publication time for system-recorded time.

Events contain opaque references and minimum necessary data. Consumers retrieve authorized details from the owning API.

## 10. Search and relationship projection

### Search channels

- exact identifier and contact lookup;
- lexical search;
- structured filters;
- semantic retrieval over approved semantic units;
- graph-neighborhood retrieval;
- recency and authoritative-source channels.

RankWeave may fuse ranked results. Raw similarity scores from different embedding spaces are never averaged. Every vector has an `embedding_space_id`, model revision, input role, origin, and creation time.

### Graph projection

The normalized relationship store is authoritative. A graph projection may be rebuilt for variable-depth relationship and organization queries. Inferred LineageWeave edges are visibly distinct and may not be promoted without review.

## 11. AI and model requirements

- Core CRUD, search filters, authorization, exports, and workflow state do not require an LLM.
- All LLM requests go through `contextual-orchestrator`.
- Prompt, provider, model, reasoning level, tool access, source references, result schema, and verification status are recorded.
- Source documents are untrusted content and cannot alter system policy or tool permissions.
- Outputs use strict JSON Schema.
- Unsupported claims are removed or marked unsupported.
- An assistant action is separated into proposal, authorization, execution, observation, and verification.
- Model fallback must preserve operation capability; chat, embeddings, image, audio, and structured outputs are not interchangeable.

## 12. Numerical model requirements

Relationship health, opportunity risk, satisfaction, forecast probability, and influence estimation are numerical products, not UI decorations.

Any released numerical model shall:

- have a stated estimand and decision use;
- define population, sampling design, error target, and failure denominator;
- use Rust production arithmetic;
- include CPU reference and GPU parity where GPU is used;
- test true-parameter recovery, bias, RMSE, interval coverage, calibration, and drift;
- account for multilevel, multiple-membership, and longitudinal structure where applicable;
- report uncertainty and allow abstention;
- preserve model, data, feature, prompt, and code lineage;
- avoid rule-of-thumb weights.

## 13. Integration requirements

Each integration implements narrow capability ports. Examples:

```text
IdentityVerificationPort
InteractionObservationPort
MessageThreadReferencePort
WorkItemReferencePort
OntologyReferencePort
RetrievalFusionPort
ModelExecutionPort
BillingEntitlementPort
```

A connector capability manifest declares read, propose, write, delete, export, webhook, and synchronization support. Provider-specific fields remain in adapter and mapping tables.

## 14. Security requirements

- Keyverse JWT signature, issuer, audience, expiry, token type, and authorization context validation.
- PostgreSQL RLS or equivalent enforced isolation.
- Dedicated runtime role with `NOSUPERUSER`, `NOBYPASSRLS`, and minimum privileges.
- Secrets resolved from approved secret management, never repository or database plaintext.
- Egress allowlist with DNS rebinding, method, host, port, size, timeout, and redirect controls.
- Structured logs redact tokens and minimize PII but do not destructively alter source records.
- Exports require purpose, field policy, bounded scope, and a signed receipt.
- Model and connector content is untrusted.

## 15. Frontend requirements

- Design tokens are the only source for repeated spacing, typography, color, elevation, and motion.
- Shared components are documented in Storybook with loading, empty, error, access-denied, stale, conflict, partial-data, and offline states.
- Figma file ID and component mapping are recorded before production UI acceptance.
- Account overview uses three horizontal bands: context, relationships, and action.
- A generic floating chat box is not the primary interface; evidence-grounded assistance is embedded in the active account or workflow context.
- Every write action has pending, success, retryable failure, and conflict states.
- No internal repository or service name appears in customer-facing copy.

## 16. Operations requirements

- Separate liveness, startup, and readiness probes.
- Readiness fails when required storage, migration compatibility, authorization material, or critical queues are unavailable.
- Graceful drain stops new work and bounds in-flight completion.
- OpenTelemetry traces, metrics, and logs use low-cardinality dimensions.
- SLOs cover interactive API, background jobs, event projection, connectors, and data-rights workflows.
- Backup, restore, key availability, and projection rebuild are rehearsed.
- Release and rollback are versioned and observable.

## 17. Build and supply-chain requirements

- Lock dependencies and verify lock freshness.
- Pin GitHub Actions by full commit SHA.
- Generate SPDX SBOM and SLSA-compatible provenance.
- Sign release artifacts and verify before promotion.
- Scan source, dependencies, images, IaC, and secrets.
- Do not run untrusted build hooks during dependency materialization.
- Reproducible build comparison is required for GA candidate artifacts.

## 18. Definition of done for a technical slice

A slice is complete only when its user behavior, domain model, API/event contract, migration, authorization, tests, telemetry, rollback, documentation, ADR impact, and product-gap status are consistent and independently reviewable.
