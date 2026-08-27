# ELUNVERA Product–Technical Gap Baseline

- **Baseline version:** 0.1
- **Observed date:** 2026-08-27
- **Repository:** `ContextualWisdomLab/ELUNVERA`
- **Target integration branch:** `develop`
- **Evidence scope:** repository metadata plus this documentation change

## 1. Executive status

ELUNVERA is a newly created public repository. Before this baseline, it contained no branches, commits, runtime, database migrations, user interface, release, checks, or production evidence. This change establishes product and technical design contracts only.

**Current honest classification:** `design baseline / pre-implementation`.

The repository must not be described as alpha, beta, production-ready, secure, compliant, scalable, accessible, or commercially validated until the corresponding implementation and evidence exist.

## 2. Product definition established by this baseline

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence system of record. It owns tenant-scoped commercial account, party, relationship, interaction metadata, commitment, opportunity, customer outcome, complaint, satisfaction observation, privacy workflow, audit, and provenance facts.

It deliberately does not own identity, email/calendar/file hosting, generalized project execution, billing, ontology/catalog, or LLM routing. Those capabilities are consumed from CWL products through versioned contracts.

## 3. Traceability matrix

| Product concern | Product requirement | Technical decision | Contract/data | Current implementation | Required next evidence |
|---|---|---|---|---|---|
| Account continuity | PRD FR-001–006 | modular account registry | `commercial_account`, account APIs | none | Rust API, migration, E2E |
| Stakeholder history | FR-010–015 | first-class bitemporal relationship | relationship tables/events | none | temporal/property/DB tests |
| Interaction context | FR-020–024 | metadata projection, source refs | interaction/commitment APIs | none | naruon/ThreadWeave contract tests |
| Opportunity truth | FR-030–036 | versioned process and immutable snapshots | opportunity tables/events | none | stage and exact-money tests |
| Complaints/outcomes | FR-040–044 | structured complaint/outcome modules | complaint/outcome APIs | none | ISO-aligned E2E evidence |
| Search/intelligence | FR-050–054 | rebuildable projection and model claims | search/model jobs | none | retrieval and unsupported-claim tests |
| Privacy/rights | FR-060–064 | purpose-aware field selection | rights/retention models | none | PIPA/GDPR profile review and E2E |
| Tenant isolation | NFR security | Keyverse + RLS | auth context | none | adversarial cross-tenant suite |
| Availability | NFR reliability | operability and restore contracts | health/SLO/runbook | none | live telemetry and restore rehearsal |
| Accessibility | NFR UX | WCAG 2.2 AA + Storybook | UX and design system | none | Figma, UI, AT audit |
| Scientific scoring | P-05 | Rust + TEPP/fast-mlsirm, no heuristics | model artifact/claim | none | validation study and model release gate |

## 4. Gap register

### G-001 Repository governance

**Gap:** no committed `develop` branch, ruleset, CODEOWNERS, required checks, labels, or release policy.
**Risk:** changes can bypass current-head review and the requested PR flow.
**Action:** establish bootstrap commit, `develop`, branch ruleset, independent approval, unresolved-thread protection, required checks, update-branch, squash merge, and branch deletion policy.
**Exit evidence:** ruleset API snapshot and tested PR.

### G-002 Executable Rust foundation

**Gap:** no Cargo workspace or production code.
**Risk:** architecture and quality goals are unverified.
**Action:** implement the M1 Rust workspace through TDD, beginning with identity/tenant context and account/party/relationship kernel.
**Exit evidence:** build, lint, unit/property/integration, coverage, and doc reports.

### G-003 PostgreSQL lifecycle

**Gap:** no migration, RLS, temporal constraint, pool, backup, or restore.
**Risk:** canonical truth and isolation are conceptual only.
**Action:** pin supported PostgreSQL 18.x, create 3NF migrations, RLS, temporal constraints, outbox, clean/upgrade rehearsal, encrypted backup, and restore validation.
**Exit evidence:** PostgreSQL integration and restore artifacts.

### G-004 Keyverse integration

**Gap:** no OIDC/JWKS/SCIM implementation.
**Risk:** no authenticated remote operation is safe.
**Action:** implement exact issuer/audience/token validation and immutable authorization context; separate CRM party identity from authentication subject.
**Exit evidence:** negative token and tenant tests.

### G-005 Account and relationship UX

**Gap:** no Figma file, design tokens, Storybook, UI, screenshots, or accessibility evidence.
**Risk:** product remains a database design rather than a usable CRM.
**Action:** create the three-band account experience in Figma, record file ID in ADR, implement shared tokens and Storybook edge states, then E2E and AT audit.
**Exit evidence:** reviewed Figma, screenshots, interaction tests, WCAG report.

### G-006 Provider and CWL contracts

**Gap:** adapters and consumer contracts do not exist.
**Risk:** integrations may duplicate authority or leak PII.
**Action:** implement one bounded vertical at a time, starting with Keyverse and then customer-controlled interaction metadata; publish provider/consumer fixtures in both repositories.
**Exit evidence:** conformance, duplicate/reorder, outage, and reconciliation tests.

### G-007 Privacy operation

**Gap:** purpose, rights, retention, hold, export, and disposition are documentation only.
**Risk:** product cannot responsibly process production customer data.
**Action:** implement policy decision receipts and complete rights/disposition workflows before production PII.
**Exit evidence:** jurisdiction-reviewed policies and realistic rights tests.

### G-008 Security and supply chain

**Gap:** no CI, SAST, secret scan, dependency review, SBOM, provenance, signatures, or penetration test.
**Risk:** no trustworthy artifact exists.
**Action:** use central `.github` reusable workflows, exact pins, minimal permissions, and signed release pipeline.
**Exit evidence:** current-head checks and signed release candidate.

### G-009 Operability

**Gap:** no health endpoints, telemetry, SLO, alert, capacity, incident, or recovery runtime.
**Risk:** failures and data loss cannot be detected or managed.
**Action:** implement liveness/startup/readiness, OTLP, low-cardinality metrics, queue/backpressure, capacity benchmark, runbooks, and rehearsal.
**Exit evidence:** SLO dashboard and operational drill receipts.

### G-010 Model governance and measurement

**Gap:** no model, dataset, benchmark, validity, fairness, or calibration evidence.
**Risk:** “relationship intelligence” could become ungrounded profiling.
**Action:** release no score until a specific outcome and population are defined; validate through contextual-orchestrator plus TEPP/fast-mlsirm where appropriate; preserve evidence, uncertainty, review, and appeal.
**Exit evidence:** model card, evaluation report, recovery/calibration metrics, monitoring.

### G-011 Commercial and legal readiness

**Gap:** no software license, trademark registration, terms, DPA, support policy, pricing, entitlement, or billing integration.
**Risk:** a public design repository is not a sellable product.
**Action:** decide license, complete trademark/legal review, define deployment/support and Billing Control Plane integration after core product evidence.
**Exit evidence:** approved legal/commercial package.

### G-012 Product validation

**Gap:** no customer interviews, usability data, activation, retention, willingness-to-pay, or outcome study.
**Risk:** engineering completeness may not create buyer value.
**Action:** validate the account-preparation, opportunity-review, and complaint-recovery verticals with target users and measure time-to-context, evidence coverage, correction rate, and workflow outcome.
**Exit evidence:** research protocol and anonymized findings.

## 5. Highest-leverage implementation order

```text
repository governance
→ identity and tenant boundary
→ PostgreSQL account/party/relationship kernel
→ audit, outbox, idempotency, temporal APIs
→ three-band account UX
→ opportunity and commitment vertical
→ complaints, outcomes, and privacy workflows
→ bounded CWL integrations
→ validated relationship intelligence
→ scale, security, accessibility, recovery, and commercial GA
```

## 6. Release truth

The documentation baseline closes the absence of a coherent product definition and implementation contract. It closes none of the runtime, security, privacy, accessibility, model-validity, scalability, operational, legal, or market-validation gaps listed above.
