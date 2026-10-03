# ADR-0004: Represent relationship truth bitemporally

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

Customer roles, account ownership, affiliations, stages, and disclosure policy change, and late evidence may describe an earlier business event.

## Decision

Store business-valid and system-recorded intervals for versioned facts. Query APIs expose temporal lens and knowledge cutoff. Corrections append versions rather than overwrite history.

## Consequences

Audits and historical reconstruction become reliable, at the cost of more complex constraints and queries.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
