# ADR-0007: Use purpose-aware field selection instead of universal masking

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

Authorized customer operations often require real names, contact details, and complaint context. Universal masking can make the product unusable, while unrestricted exposure violates minimization.

## Decision

Evaluate tenant, actor, role, purpose, data category, relationship context, disclosure policy, and legal hold. Return only allowed fields and retain decision receipts.

## Consequences

Operational work remains possible with auditable protection. Policy design and testing become first-class product work.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
