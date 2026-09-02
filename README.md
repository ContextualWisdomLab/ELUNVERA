# ELUNVERA

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ContextualWisdomLab/ELUNVERA)

> **Every Link, Understood. Every Relationship, Activated.**

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence platform. It gives customer-facing teams a governed system of record for commercial accounts, stakeholders, interactions, commitments, opportunities, customer outcomes, and the decisions that connect them.

ELUNVERA is not an email host, a calendar server, an ERP, a billing engine, a project-management suite, or an autonomous sales agent. It composes those capabilities through explicit ContextualWisdomLab contracts while preserving a narrow source-of-truth boundary.

## Product promise

ELUNVERA helps a user answer four questions without reconstructing context manually:

1. **What changed in this relationship?**
2. **Why does it matter now?**
3. **What commitment or decision is at risk?**
4. **What is the next defensible action, and what evidence supports it?**

## Initial product boundary

ELUNVERA owns:

- tenant-scoped commercial accounts and account-role history;
- people, organizations, contact points, and time-valid relationship facts;
- account-team assignments;
- interaction and evidence references;
- commitments and relationship actions;
- opportunities, stage history, stakeholder participation, values, and forecast snapshots;
- customer outcomes, complaints, satisfaction observations, and relationship assessments;
- purpose, communication preference, retention, audit, and data-rights workflow metadata.

ELUNVERA consumes but does not own:

- identity and federation from **Keyverse**;
- customer-owned email, calendar, and file interaction from **naruon**;
- RFC email threading from **ThreadWeave**;
- inferred record lineage from **LineageWeave**;
- retrieval fusion from **RankWeave**;
- LLM routing and evaluation from **contextual-orchestrator**;
- temporal measurement from **TEPP** and psychometric calibration from **fast-mlsirm**;
- ontology and catalog context from **semantic-data-portal**;
- generalized project and issue execution from **ScopeWeave**;
- commercial entitlement and billing truth from **billing-control-plane**.

## Documentation map

| Document | Purpose |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | Product vision, users, requirements, scope, and release criteria |
| [`docs/TRD.md`](docs/TRD.md) | Technical requirements and platform constraints |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System boundaries, components, trust zones, and deployment model |
| [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) | Canonical entities, temporal facts, ERD, and data invariants |
| [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md) | HTTP, event, idempotency, pagination, and compatibility contracts |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Security architecture and control baseline |
| [`docs/PRIVACY.md`](docs/PRIVACY.md) | Purpose limitation, data rights, retention, and disclosure rules |
| [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) | Assets, actors, abuse cases, and mitigations |
| [`docs/TEST_STRATEGY.md`](docs/TEST_STRATEGY.md) | TDD, coverage, contract, security, and realistic validation |
| [`docs/OPERABILITY.md`](docs/OPERABILITY.md) | SLOs, telemetry, backup, restoration, and incident response |
| [`docs/UX_SPEC.md`](docs/UX_SPEC.md) | Customer-facing information architecture and interaction principles |
| [`docs/product-technical-gap-baseline.md`](docs/product-technical-gap-baseline.md) | Current implementation truth and prioritized gaps |
| [`docs/adr/README.md`](docs/adr/README.md) | Architecture decision index |
| [`docs/doctoring/REFERENCES.md`](docs/doctoring/REFERENCES.md) | APA 7th research and standards bibliography |
| [`LICENSE`](LICENSE) | Apache License 2.0 grant for ELUNVERA-authored source and documentation |

## Development status

This repository currently contains a **documentation and contract baseline only**. No production service, database migration, UI, connector, benchmark result, certification, or release claim exists yet. The implementation sequence is defined in [`docs/ROADMAP.md`](docs/ROADMAP.md) and the executable plan in [`docs/superpowers/plans/2026-08-27-elunvera-foundation-implementation-plan.md`](docs/superpowers/plans/2026-08-27-elunvera-foundation-implementation-plan.md).

## Working conventions

- Primary integration branch: `main`
- Review flow: feature branch → current-head checks → independent review → squash merge
- Database object names: two or more words in `snake_case`
- Production arithmetic and model computation: Rust
- API source: OpenAPI 3.2.0
- Event source: AsyncAPI 3.1.0 with CloudEvents 1.0 envelopes
- Database baseline: PostgreSQL 18.6 or later supported 18.x security release
- Accessibility target: WCAG 2.2 AA
- Quality target for shipped ELUNVERA-owned code: 100% production statement coverage, 100% production branch coverage, and 100% public API documentation coverage

## License

ContextualWisdomLab-authored ELUNVERA source and documentation are licensed under the [Apache License 2.0](LICENSE). The license grant does not assert trademark registration and does not relicense third-party standards, dependencies, generated assets, datasets, models, provider services, or future imported material. Those components retain their own terms and require independent provenance and commercial-license review before incorporation or distribution.
