# ADR-0010: Use Rust for production computation and prohibit heuristic scores

- **Status:** Proposed
- **Date:** 2026-08-27
- **Decision owners:** ELUNVERA maintainers

## Context

Commercial scoring, temporal measurement, vector/matrix work, and performance-critical paths require predictable safety and concurrency. Arbitrary weighted scores are not defensible.

## Decision

Implement ELUNVERA production logic and numerical kernels in Rust. Use TEPP or fast-mlsirm for research-backed measurement where applicable. Do not ship undocumented rule-of-thumb probabilities or health scores.

## Consequences

Performance and reproducibility improve. Scientific model development has a higher evidence burden, which is intentional.

## Compliance and verification

The decision is enforced through contract, migration, unit, integration, security, and documentation tests appropriate to the affected boundary. A conflicting implementation requires a superseding ADR before merge.
