# ELUNVERA API and Event Contract

- **Document version:** 0.1
- **Status:** Proposed contract baseline
- **Date:** 2026-08-27

## 1. Contract objectives

ELUNVERA exposes versioned HTTP and event contracts that preserve tenant isolation, temporal truth, idempotency, provenance, and provider independence. The contracts describe target behavior; no endpoint is implemented by this documentation baseline.

## 2. Contract sources

- HTTP source: `schemas/openapi.yaml`, OpenAPI 3.2.0.
- Event source: `schemas/asyncapi.yaml`, AsyncAPI 3.1.0.
- Payload schemas: JSON Schema Draft 2020-12 under `schemas/events/`.
- Error representation: RFC 9457 Problem Details.
- Event envelope: CloudEvents 1.0.

Generated SDKs may be published only from a tagged, validated contract revision. Hand-maintained clients are not authoritative.

## 3. Authentication and request context

Every authenticated request carries a Keyverse-issued bearer token. The API validates issuer, audience, signature, token type, time bounds, and required claims before constructing this immutable context:

```text
actor_reference
principal_kind_code
tenant_reference
workspace_reference
role_set
scope_set
purpose_code
decision_reference
correlation_id
authentication_strength
token_issued_at
token_expires_at
```

A caller-supplied `tenant_id`, role, purpose, or actor header never overrides verified claims. Service-to-service calls use a service principal and an explicit delegated purpose.

## 4. Common HTTP rules

### 4.1 Base and media types

- Base path: `/v1`.
- Default request and response media type: `application/json`.
- Export formats use explicit versioned media types.
- UTF-8 is mandatory.
- Unknown top-level fields are rejected for commands unless the schema explicitly permits extensions.

### 4.2 Request identity

Mutating operations require:

```http
Idempotency-Key: 019d4b72-507c-71a8-9026-1b82067f40f1
X-Correlation-Id: 019d4b72-507c-71a8-9026-1b82067f40f2
```

The server stores the key, canonical request hash, operation status, response reference, and expiration policy. Replaying the same key with the same canonical payload returns the original receipt. Reusing the key with a different payload returns `409 Conflict`.

### 4.3 Concurrency

Editable aggregates return an ETag. A command that changes an existing aggregate requires `If-Match`. A stale version returns `412 Precondition Failed` and does not apply a partial change.

### 4.4 Pagination

Collection endpoints use opaque cursor pagination:

```json
{
  "items": [],
  "next_cursor": "opaque-value-or-null",
  "page_size": 50
}
```

Ordering is deterministic. A cursor binds the tenant, filter, sort, and knowledge cutoff. Page size is bounded by the contract.

### 4.5 Time and knowledge cutoff

Temporal reads may specify `valid_at`, `recorded_at`, or `knowledge_cutoff`. The response echoes the effective temporal lens. The server does not use facts recorded after the requested knowledge cutoff.

### 4.6 Long-running operations

Imports, exports, bulk merges, model evaluations, and large relationship projections return `202 Accepted` with a durable `job_reference`. Job states are:

```text
accepted → queued → running → succeeded
                    ├→ failed
                    └→ cancellation_requested → cancelled | succeeded
```

The cancellation receipt states whether execution stopped before work, during work, or after completion.

## 5. Problem Details

Every non-success response uses RFC 9457 fields and ELUNVERA extensions:

```json
{
  "type": "urn:elunvera:problem:stale-aggregate",
  "title": "The record changed before this update was applied.",
  "status": 412,
  "detail": "Refresh the account and review the latest changes before saving again.",
  "instance": "urn:elunvera:operation:019d...",
  "error_code": "stale_aggregate",
  "correlation_id": "019d...",
  "safe_next_action": "refresh_and_compare"
}
```

Messages help the user take the next action and never expose SQL, internal service names, stack traces, secrets, or cross-tenant existence.

## 6. Contract-bearing P0 endpoints

The authoritative P0 HTTP surface is exactly the set of operations present in `schemas/openapi.yaml`:

```text
GET    /v1/accounts
POST   /v1/accounts
GET    /v1/accounts/{account_id}
PATCH  /v1/accounts/{account_id}
POST   /v1/relationships
POST   /v1/opportunities/{opportunity_id}/stage-transitions
```

The two account read operations accept the contract-defined `valid_at`, `recorded_at`, and `knowledge_cutoff` parameters and echo the effective temporal lens in response headers. Mutations require `X-Correlation-Id` and `Idempotency-Key`; updates to an existing aggregate also require `If-Match`.

Parties, interactions, commitments, relationship review, account merge/split, customer outcomes, complaints, satisfaction observations, search, model jobs, privacy cases, disposition, legal hold, and audit-query operations remain product-roadmap candidates. They are **not** HTTP contract commitments until their operations and schemas are added to `schemas/openapi.yaml`, validated, and versioned.

Model-related future operations must return evidence references, uncertainty, model identity, prompt hash, and review status. A model claim can never mutate authoritative CRM facts without an explicit human-reviewed command.

## 7. Command receipts

A successful mutation returns a stable receipt rather than relying only on an HTTP status:

```json
{
  "operation_id": "019d...",
  "aggregate_reference": "urn:elunvera:tenant:account:019d...",
  "aggregate_version": 7,
  "recorded_at": "2026-08-27T09:00:00Z",
  "event_reference": "urn:elunvera:event:019d...",
  "idempotency_status": "new"
}
```

Receipts are queryable and included in audit evidence.

## 8. Event envelope

Domain events include the CloudEvents core fields plus bounded extensions:

```json
{
  "specversion": "1.0",
  "id": "019d...",
  "source": "urn:elunvera:tenant_001",
  "type": "org.contextualwisdomlab.elunvera.relationship.changed.v1",
  "subject": "urn:elunvera:tenant_001:relationship:019d...",
  "time": "2026-08-27T09:00:00Z",
  "datacontenttype": "application/json",
  "tenantref": "urn:elunvera:tenant_001",
  "correlationid": "019d...",
  "causationid": "019d...",
  "provenanceref": "urn:elunvera:evidence:019d...",
  "purposecode": "account_management",
  "dataclassification": "restricted_personal_and_commercial",
  "schemarevision": "1.0.0",
  "data": {
    "recorded_at": "2026-08-27T08:59:58Z"
  }
}
```

Events never contain passwords, tokens, raw email bodies, unrestricted notes, unnecessary contact details, or provider secrets.

`time` is the CloudEvent publication time. Payloads that carry bitemporal facts include an explicit immutable `recorded_at`, because an outbox or broker delay can make publication time later than the system-recorded time. The internal metadata names `data_classification` and `schema_revision` serialize as the CloudEvents extension attributes `dataclassification` and `schemarevision`.

## 9. Initial event types

```text
account.created.v1
account.changed.v1
account.merged.v1
account.split.v1
party.changed.v1
relationship.changed.v1
relationship.reviewed.v1
interaction.recorded.v1
commitment.changed.v1
opportunity.changed.v1
opportunity.stage_changed.v1
forecast_snapshot.recorded.v1
complaint.changed.v1
satisfaction_observation.recorded.v1
model_claim.proposed.v1
model_claim.reviewed.v1
data_rights_case.changed.v1
disposition.completed.v1
```

An event type is immutable. A breaking payload change creates a new major suffix.

## 10. Consumer rules

- Delivery is at least once.
- Consumers deduplicate by `(source, id)` and persist an inbox receipt.
- Consumers validate schema before applying a projection.
- Processing and its projection receipt commit atomically.
- Poison messages move to a dead-letter workflow without blocking unrelated tenant events.
- A consumer never upgrades `inferred` or `proposed` truth to `authoritative` automatically.

## 11. Provider adapters

Integrations use capability-specific ports such as `interaction_observation_port`, `calendar_commitment_port`, `identity_resolution_port`, `billing_entitlement_port`, and `work_execution_port`. Core tables do not acquire columns such as `salesforce_id`, `hubspot_id`, or `stripe_customer_id`; mappings live in `external_object_mapping`.

## 12. Compatibility policy

- Additive optional fields require a minor contract version.
- Removing a field, tightening an enum, or changing semantics requires a new major API or event version.
- A deprecated field remains supported for at least two minor releases and one documented migration window.
- Schema changes include positive, negative, and backward-compatibility fixtures.
- Provider and consumer contract tests run in both owning repositories.
