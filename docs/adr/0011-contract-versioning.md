# ADR-0011: Version HTTP and events independently

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

Consumers need stable contracts across deployment and provider changes. HTTP resources and asynchronous facts evolve at different rates.

## Decision

OpenAPI 3.2.0 is the HTTP source, AsyncAPI 3.1.0 the event source, JSON Schema 2020-12 the payload source, CloudEvents 1.0 the envelope, and RFC 9457 the error format. Breaking changes create a new major version.

## Consequences

SDK generation and compatibility tests are possible. Contract review becomes a release gate.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
