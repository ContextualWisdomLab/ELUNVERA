# Changelog

All notable changes to ELUNVERA will be documented in this file.

The format follows Keep a Changelog principles, and versioning will begin when the first executable release candidate exists.

## [Unreleased]

### Added

- Initial ELUNVERA product and technical documentation baseline.
- Product requirements, technical requirements, architecture, data model, API and event contracts.
- Security, privacy, threat-model, testing, operability, UX, user-story, use-case, storyboard, wireframe, and Storybook baselines.
- Architecture decision record set covering product ownership, modularity, identity, tenancy, temporal facts, relationships, integrations, privacy, AI, persistence, APIs, quality, UX, retention, and ecosystem boundaries.
- OpenAPI 3.2.0 and AsyncAPI 3.1.0 draft contracts.
- Initial product-technical gap baseline and phased implementation plan.
- Public documentation landing and exact-cased DeepWiki entry point.
- Apache License 2.0 grant for ContextualWisdomLab-authored ELUNVERA source and documentation, with trademark and third-party rights kept separate.

### Fixed

- Aligned the narrative HTTP inventory with the authoritative OpenAPI P0 surface.
- Added temporal read parameters and effective-lens response headers to the machine-readable HTTP contract.
- Corrected AsyncAPI operations to publish ELUNVERA domain events and required classification/schema metadata.
- Added explicit `recorded_at` payload fields so outbox publication delay cannot corrupt bitemporal reconstruction.
- Removed one-shot reconciliation/review-repair workflows and script from the publishable candidate before final manifest sealing.
- Retargeted the Draft foundation to canonical protected `main`, aligned document-contract and review automation with that base, and corrected stale `develop` navigation/governance claims.
- Returned ADR-0013 to `Proposed` while the foundation remains unmerged; protected integration is required before the decision may be marked `Accepted`.
- Aligned AGENTS, contributing guidance, PRD, roadmap, and implementation plan/spec branch authority with canonical protected `main`; stacked work may target only its verified prerequisite branch, and document-contract CI now guards that authority against drift.

### Security

- Defined fail-closed tenant isolation, purpose-aware authorization, immutable audit, model provenance, controlled egress, and customer-data disclosure boundaries.

### Notes

- No runtime, database schema, deployment artifact, or release exists in this baseline.
