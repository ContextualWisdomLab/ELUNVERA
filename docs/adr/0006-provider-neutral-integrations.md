# ADR-0006: Use capability-specific integration ports

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

Providers differ materially and a generic “CRM provider” interface collapses important semantics. Provider IDs in core tables create schema coupling.

## Decision

Define small capability ports, preserve external object mappings in a dedicated table, journal commands, and normalize inbound assertions only after validation.

## Consequences

Providers can change without rewriting canonical CRM tables. More adapters and contract tests are required.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
