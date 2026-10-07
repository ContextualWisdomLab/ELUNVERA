# ADR-0001: Own CRM truth; federate adjacent products

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

ELUNVERA needs a defensible source-of-truth boundary in the CWL ecosystem. A full-suite CRM would duplicate identity, mail, calendar, billing, project management, ontology, and model orchestration.

## Decision

ELUNVERA owns commercial accounts, parties within tenant context, first-class relationships, interactions metadata, commitments, opportunities, customer outcomes, complaints, satisfaction observations, privacy workflow metadata, and their audit history. Adjacent CWL products remain authoritative for their domains and integrate through explicit ports and events.

## Consequences

The CRM remains coherent and reusable. Integration contracts require more design work than direct database access, but prevent a distributed monolith.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
