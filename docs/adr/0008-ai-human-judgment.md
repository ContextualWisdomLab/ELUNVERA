# ADR-0008: Separate model claims from authoritative facts

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

LLMs can synthesize evidence but may hallucinate, inherit bias, or misinterpret context. Direct mutation would turn probabilistic output into hidden commercial truth.

## Decision

Route LLM work through contextual-orchestrator. Store output as `model_claim` with model, prompt, evidence, uncertainty, validation, and review status. Consequential domain changes require a separate human-authorized command.

## Consequences

AI assistance remains useful and inspectable. Some automation is intentionally slower because review is explicit.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
