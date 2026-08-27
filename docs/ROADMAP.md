# ELUNVERA Delivery Roadmap

## M0 — Documentation and contract baseline

**Exit criteria**

- PRD, TRD, architecture, data model, security, privacy, threat model, UX, test, operability, ADR, OpenAPI, AsyncAPI, and schemas reviewed;
- product boundary accepted;
- no implementation or readiness claim mixed into documentation;
- `develop` integration branch and protected review policy established.

## M1 — Identity, tenancy, and canonical CRM kernel

- Rust workspace and repository quality gates;
- Keyverse OIDC context;
- tenant, workspace, member, party, account, and first-class relationship model;
- PostgreSQL 18.6 migration and RLS;
- audit, idempotency, ETag, outbox, and operation receipt;
- account overview read model without LLM dependency.

**Buyer outcome:** governed account and stakeholder history.

## M2 — Interaction, commitment, and opportunity vertical

- manual and normalized interaction metadata;
- commitment lifecycle;
- versioned sales process and opportunity history;
- exact money and forecast snapshots;
- timeline and account three-band UI;
- import dry-run and provider mapping.

**Buyer outcome:** auditable opportunity progression and protected promises.

## M3 — Complaints, outcomes, and privacy operations

- complaint and remedy workflow;
- desired and observed customer outcomes;
- satisfaction observation registry;
- communication preference and processing-basis references;
- rights cases, export manifests, retention, hold, and disposition.

**Buyer outcome:** closed-loop service recovery and governed customer data.

## M4 — CWL context integrations

- naruon observation and action-reference adapter;
- ThreadWeave and LineageWeave evidence projection;
- RankWeave search fusion;
- Semantic Data Portal ontology references;
- ScopeWeave work-execution reference;
- Billing Control Plane entitlement reference;
- reconciliation and connector operability.

**Buyer outcome:** scattered context connected without duplicating source authorities.

## M5 — Calibrated relationship intelligence

- contextual-orchestrator model jobs;
- evidence-grounded meeting briefs and proposed claims;
- model registry, claim review, and provider/prompt trace;
- TEPP and fast-mlsirm integration for validated temporal or measurement use cases;
- true-parameter, calibration, fairness, and uncertainty evidence;
- no heuristic score fallback.

**Buyer outcome:** explainable assistance rather than opaque CRM scoring.

## M6 — Enterprise scale and GA

- multi-region or customer-isolated deployment profiles;
- 100,000 accounts and 10,000,000 relationship/interaction facts benchmark profile;
- k6 load and hot-partition remediation;
- external security review and penetration test;
- backup/restore, key rotation, incident, upgrade, and rollback evidence;
- WCAG 2.2 AA audit;
- signed OCI artifacts, SPDX SBOM, provenance, release notes, and support policy;
- commercial packaging and billing integration.

## Sequencing rules

- Do not implement intelligence before canonical account, relationship, temporal, and evidence contracts.
- Do not implement a graph as the source of truth.
- Do not expose production PII before identity, tenant, purpose, audit, retention, and restore gates.
- Do not call a feature GA because a document or demo exists.
- Each milestone is split into independently reviewable vertical PRs and keeps the product usable at the end of the slice.
