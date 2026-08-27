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

## 6. Resource endpoints

The initial contract surface is deliberately narrow.

### Accounts

```text
POST   /v1/accounts
GET    /v1/accounts/{account_id}
PATCH  /v1/accounts/{account_id}
GET    /v1/accounts
GET    /v1/accounts/{account_id}/timeline
GET    /v1/accounts/{account_id}/relationships
POST   /v1/accounts/{account_id}/merge-jobs
POST   /v1/accounts/{account_id}/split-jobs
```

### Parties and relationships

```text
POST   /v1/parties
GET    /v1/parties/{party_id}
PATCH  /v1/parties/{party_id}
POST   /v1/relationships
GET    /v1/relationships/{relationship_id}
PATCH  /v1/relationships/{relationship_id}
POST   /v1/relationships/{relationship_id}/review-decisions
```

### Interactions and commitments

```text
POST   /v1/interactions
GET    /v1/interactions/{interaction_id}
POST   /v1/commitments
PATCH  /v1/commitments/{commitment_id}
POST   /v1/commitments/{commitment_id}/transitions
```

### Opportunities

```text
POST   /v1/opportunities
GET    /v1/opportunities/{opportunity_id}
PATCH  /v1/opportunities/{opportunity_id}
POST   /v1/opportunities/{opportunity_id}/stage-transitions
POST   /v1/opportunities/{opportunity_id}/value-snapshots
POST   /v1/opportunities/{opportunity_id}/forecast-snapshots
```

### Customer outcomes and complaints

```text
POST   /v1/customer-outcomes
GET    /v1/customer-outcomes/{outcome_id}
POST   /v1/complaints
GET    /v1/complaints/{complaint_id}
POST   /v1/complaints/{complaint_id}/transitions
POST   /v1/satisfaction-observations
```

### Search and proposed intelligence

```text
POST   /v1/search-queries
POST   /v1/context-bundles
POST   /v1/model-jobs
GET    /v1/model-jobs/{job_id}
POST   /v1/model-claims/{claim_id}/review-decisions
```

Model endpoints return evidence references, uncertainty, model identity, prompt hash, and review status. A model claim cannot mutate authoritative CRM facts.

### Privacy and audit

```text
POST   /v1/data-rights-cases
GET    /v1/data-rights-cases/{case_id}
POST   /v1/data-rights-cases/{case_id}/exports
POST   /v1/disposition-jobs
POST   /v1/legal-holds
GET    /v1/audit-events
```

Audit search is purpose-restricted and paginated. Export manifests identify included and excluded fields, source authority, and policy reason.

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
  "data": {}
}
```

Events never contain passwords, tokens, raw email bodies, unrestricted notes, unnecessary contact details, or provider secrets.

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
