# ADR-0009: Use PostgreSQL 18 as canonical system of record

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

CRM transactions need strong consistency, temporal constraints, row-level isolation, exact money, and recoverable history.

## Decision

Use a normalized PostgreSQL 18.6-or-later supported 18.x database. Search, graph, vector, and analytics stores are rebuildable projections. Use UUIDv7 and transactional outbox.

## Consequences

The canonical layer is robust and portable. Projection rebuild and database lifecycle require operational investment.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
