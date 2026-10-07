# ADR-0012: Require evidence-based release gates

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

A documentation-rich or test-heavy repository can still ship broken behavior if current-head, realistic, security, migration, and recovery evidence is missing.

## Decision

Require 100% ELUNVERA-owned production statement and branch coverage, 100% public API documentation, current-head checks, realistic PostgreSQL and E2E tests, supply-chain evidence, migration and restore rehearsal, and independent review.

## Consequences

Release confidence is evidence-backed. CI cost and review time increase and must be managed rather than bypassed.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
