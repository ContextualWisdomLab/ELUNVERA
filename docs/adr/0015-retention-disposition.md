# ADR-0015: Make retention, legal hold, and disposition explicit workflows

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

CRM data cannot be kept indefinitely or deleted through ad hoc database operations. Historical and legal obligations differ by record class.

## Decision

Version retention policies, represent legal holds, execute bounded disposition jobs with dry-run and item receipts, and preserve minimal deletion proof. Destructive bulk actions require maker-checker approval.

## Consequences

Privacy and auditability improve. Storage and disposition orchestration become product responsibilities.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
