# ELUNVERA

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence platform for governed commercial accounts, stakeholders, interactions, commitments, opportunities, customer outcomes, and the decisions that connect them.

[Ask DeepWiki](https://deepwiki.com/ContextualWisdomLab/ELUNVERA)

## Start here

- [Repository README](https://github.com/ContextualWisdomLab/ELUNVERA/blob/develop/README.md) — product promise, bounded responsibility, development status, and documentation map.
- [Product requirements](PRD.md) — users, jobs, requirements, scope, and release criteria.
- [Technical requirements](TRD.md) — platform constraints and implementation contracts.
- [Architecture](ARCHITECTURE.md) — bounded contexts, components, trust zones, and deployment model.
- [Canonical data model](DATA_MODEL.md) — temporal commercial facts, entities, ERD, and invariants.
- [API contract](API_CONTRACT.md) — HTTP, events, idempotency, pagination, concurrency, and compatibility.
- [Security](SECURITY.md) and [threat model](THREAT_MODEL.md) — product security boundaries and abuse-case treatment.
- [Privacy](PRIVACY.md) — purpose limitation, communication preferences, retention, disclosure, and data-rights workflows.
- [Test strategy](TEST_STRATEGY.md) — TDD, contract, security, coverage, and realistic validation expectations.
- [Operability](OPERABILITY.md) — SLO, telemetry, backup, recovery, and incident-response expectations.
- [UX specification](UX_SPEC.md) — information architecture and interaction principles.
- [Architecture decisions](adr/README.md) — accepted and proposed product/technical decisions.
- [Product/technical gap baseline](product-technical-gap-baseline.md) — current evidence, missing capabilities, and next actions.
- [Research and standards references](doctoring/REFERENCES.md) — APA-style source register.
- [Apache License 2.0](https://github.com/ContextualWisdomLab/ELUNVERA/blob/develop/LICENSE) — repository grant for ContextualWisdomLab-authored source and documentation.

## Product boundary

ELUNVERA owns tenant-scoped commercial relationship truth and its evidence, review state, temporal history, privacy metadata, opportunities, commitments, outcomes, complaints, and satisfaction observations. Identity and federation remain owned by Keyverse; mail, calendar, and file interaction remain with the products that originate them; reusable threading, lineage, retrieval fusion, model routing, psychometrics, ontology/catalog, generalized project execution, and billing retain their own ContextualWisdomLab authorities.

Model output is evidence for review, not an automatic mutation of authoritative CRM truth. Graph, search, and vector representations are projections over the canonical governed record rather than competing systems of record.

## Current maturity

The current reviewed source is a documentation and machine-readable contract baseline. It does not, by itself, prove an implemented production service, database migration, hosted user interface, benchmark, security certification, accessibility conformance, customer deployment, or release. Those claims require executable artifacts and current-head verification evidence.

## Onboarding and verification

Begin with the PRD, TRD, architecture, data model, and API contract before implementing a product slice. The repository's permanent document/contract workflow and current protected-branch checks remain the integration authority. Any implementation must preserve the documented bitemporal/evidence model, normalized PostgreSQL system-of-record boundary, explicit service contracts, accessibility target, and security/privacy constraints.

## License and rights boundary

ContextualWisdomLab-authored ELUNVERA source and documentation are licensed under Apache License 2.0. That grant does not assert trademark registration and does not relicense standards, dependencies, generated assets, datasets, models, provider services, or future imported material. Those components remain subject to independent provenance, commercial-license compatibility, and attribution review.

## Releases and deeper exploration

- [GitHub Releases](https://github.com/ContextualWisdomLab/ELUNVERA/releases)
- [Ask DeepWiki](https://deepwiki.com/ContextualWisdomLab/ELUNVERA)
- [ContextualWisdomLab](https://github.com/ContextualWisdomLab)

This is a public documentation landing source. GitHub Pages is considered published only after the source is integrated to the protected default branch, repository settings and deployment succeed, and the live HTTPS content is verified.
