# ADR-0002: Begin as a modular monolith

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

The domain is new, its consistency boundaries are not yet measured, and premature service decomposition would require distributed transactions.

## Decision

Start with independently testable Rust modules, one canonical PostgreSQL system of record, durable workers, and a transactional outbox. Extract a service only when workload, release cadence, regulatory isolation, or ownership evidence justifies it.

## Consequences

Strong local transactions and simpler operations are preserved. Module boundaries and contracts must still be enforced in code and tests.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
