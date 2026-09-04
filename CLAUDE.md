# CLAUDE.md — ELUNVERA repository context

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence system of record.

## North-star behavior

Turn scattered customer context into a judgment-ready structure and an evidence-linked next action. Do not produce generic summaries or opaque scores.

## Canonical boundaries

- Keyverse owns identity and federation.
- naruon owns interaction with customer-controlled email, calendar, and files.
- ThreadWeave computes email threads.
- LineageWeave proposes inferred lineage.
- ScopeWeave owns generalized work and project execution.
- Billing Control Plane owns commercial metering, entitlement, invoices, and payment truth.
- Semantic Data Portal owns cross-product ontology and catalog context.
- ELUNVERA owns customer relationship, commercial account, opportunity, commitment, complaint, and customer-outcome facts.

## Non-negotiable implementation constraints

- Rust-first backend and compute boundary.
- PostgreSQL 18.6+ within supported 18.x.
- 3NF canonical store; graph/search/vector views are projections.
- Tenant isolation enforced in application and database layers.
- Purpose-aware access and field selection; no destructive masking of authorized operational data.
- Bitemporal relationship and role history.
- Exact decimal money; no binary floating-point monetary calculations.
- No heuristic relationship-health or forecast weights.
- Human authority for irreversible customer-facing actions.
- Full provenance for model-generated claims.
- 100% production statement/branch/doc coverage for ELUNVERA-owned shipped code.

Read `AGENTS.md` and the product/technical documents before making changes.
