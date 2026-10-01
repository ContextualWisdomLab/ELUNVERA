# ADR-0014: Use a three-band account UX and shared design system

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

CRM dashboards often fragment account truth into unrelated cards and expose implementation boundaries. Relationship graphs alone are inaccessible and hard to act on.

## Decision

Structure account overview into context, relationship structure, and action/risk bands. Create a Figma library, source-controlled design tokens, Storybook inventory, exact-value alternatives, Korean/English copy, and WCAG 2.2 AA evidence.

## Consequences

The interface follows the user’s decision flow. Design-system and accessibility work are mandatory before UI completion.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
