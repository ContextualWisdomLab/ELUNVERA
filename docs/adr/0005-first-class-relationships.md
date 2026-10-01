# ADR-0005: Make relationships first-class records

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

A bare graph edge cannot carry evidence, confidence, temporal validity, context, disclosure policy, review state, or multiple participants.

## Decision

Use normalized `relationship_record` and `relationship_participant` objects. Graph views are rebuildable projections of canonical records.

## Consequences

Context-rich relationships and multi-party roles are supported. Projection lag and relational-to-graph mapping require observability.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
