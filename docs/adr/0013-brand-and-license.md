# ADR-0013: Preserve ELUNVERA brand and defer code license decision

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

The brand was selected through preliminary domain and clearance review, but formal trademark registration and software licensing are separate decisions.

## Decision

Use `ELUNVERA`/`Elunvera` and Korean `엘룬베라` consistently. Do not claim trademark registration. Do not accept distributable source code until the repository license is decided and documented.

## Consequences

Brand consistency is protected without making unsupported legal claims. Implementation is gated on a license decision.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
