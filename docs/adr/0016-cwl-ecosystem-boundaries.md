# ADR-0016: Integrate CWL products without direct SQL or code copying

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

CWL components have distinct authoritative responsibilities and maturity. Copying code or reading another product database would create inconsistent truth and release coupling.

## Decision

Use released packages for small stateless libraries and versioned APIs/events for stateful products. Prohibit service-to-service direct SQL. Record each dependency’s maturity and fallback behavior.

## Consequences

The ecosystem remains modular and independently releasable. Integration availability and contract drift require explicit monitoring.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
