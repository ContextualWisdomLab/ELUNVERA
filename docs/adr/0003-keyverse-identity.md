# ADR-0003: Use Keyverse as identity authority

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

ELUNVERA must not become another password store and must participate in CWL federation and SCIM lifecycle.

## Decision

Validate Keyverse OIDC/OAuth 2.1 tokens and consume SCIM lifecycle. Keep CRM party identity separate from authentication subject identity. Store opaque links, not credentials.

## Consequences

Authentication and workforce/customer identity remain distinct. Availability depends on token validation material and a reviewed degraded-mode policy.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
