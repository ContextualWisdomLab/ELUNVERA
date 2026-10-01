# ELUNVERA Product–Technical Gap Baseline

- **Baseline version:** 0.6
- **Observed date:** 2026-10-01
- **Repository:** `ContextualWisdomLab/ELUNVERA`
- **Target integration branch:** `main`
- **Evidence scope:** live repository/PR state plus this Draft foundation's PRD, TRD, architecture, data model, API/event contracts, UX, test strategy, ADRs, and source-license proposal

## 1. Executive status

ELUNVERA is a public, non-fork, very-early-stage repository whose protected `main` branch remains at the bootstrap revision. This Draft now preserves both valid deltas: the product/technical foundation and the executable relationship-activation prototype. The loopback Python server, in-memory queue, and static browser surface start empty and use anonymized fixtures only in tests. They are not the Rust/PostgreSQL production boundary. No production runtime, database migration, customer deployment, benchmark, protected-main integration, or immutable release exists.

**Current honest classification:** `integrated Draft foundation plus executable prototype / pre-production`.

The repository must not be described as alpha, beta, production-ready, secure, compliant, scalable, accessible, internationally complete, or commercially validated until the corresponding implementation and evidence exist. Current exact-head workflow/review status belongs to the live PR evidence and must be re-fetched after every push; queued, skipped, startup-failed, or predecessor-head results are not passing evidence.

## 2. Product definition and DDD boundary

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence system of record. Its **core subdomain** is governed commercial relationship truth and action: tenant-scoped commercial accounts, parties, relationships, interactions, commitments, opportunities, customer outcomes, complaints, privacy workflow, audit, and evidence-linked human decisions.

Supporting subdomains include authorization-context consumption, integration mapping/outbox, search projections, model evidence, and ELUNVERA-owned UI translation resources. Generic capabilities such as identity, LLM routing, ontology/catalog publication, retrieval fusion, message threading, and general work execution remain with their released ContextualWisdomLab owners and are consumed only through versioned contracts and ACLs.

### Bounded contexts and context map

```text
Keyverse ──ACL──> Authorization Context
                    │
                    v
Account Registry <──> Party Registry <──> Relationship Registry
       │                    │                    │
       ├──────────────> Interaction Timeline <──┤
       ├──────────────> Commitment Registry <───┤
       └──────────────> Opportunity Management ─┤
                                             Customer Outcomes / Complaints
                                                      │
                          Privacy Rights <─────────────┤
                          Audit & Provenance <─────────┤
                          Translation Resources ───────┤
                                                      v
                 rebuildable Search / Model Evidence / Integration Outbox
                         │              │                │
                         v              v                v
                   RankWeave     contextual-orchestrator   released provider/CWL APIs
```

The aggregate boundary is the smallest transactionally consistent business object; ELUNVERA does not create a shared-kernel monolith across account, relationship, opportunity, privacy, translation, or external products. External/legacy dependencies are isolated behind ACLs. Translation resource publication is separate from ontology label publication and never changes product-domain ubiquitous language.

## 3. Traceability matrix

| Product concern | Product requirement | Technical decision | Contract/data | Current implementation | Required next evidence |
|---|---|---|---|---|---|
| Account continuity | PRD FR-001–005 | modular account registry | `commercial_account`, account APIs | none | Rust API, migration, E2E |
| Stakeholder history | FR-010–013 | first-class bitemporal relationship | relationship tables/events | loopback Activation Queue prototype is integrated with the Draft foundation; it remains in-memory and non-tenant-aware | Rust domain boundary, temporal/property/DB tests, and protected integration |
| Interaction context | FR-020–024 | metadata projection, source refs | interaction/commitment APIs | none | released provider/CWL contract tests |
| Opportunity truth | FR-030–035 | versioned process and immutable snapshots | opportunity tables/events | none | stage and exact-money tests |
| Complaints/outcomes | FR-040–043 | structured complaint/outcome modules | complaint/outcome APIs | none | ISO-aligned E2E evidence |
| Search/intelligence | FR-050–053 | rebuildable projection and model claims | search/model jobs | none | retrieval and unsupported-claim tests |
| Privacy/rights | FR-060–064 | purpose-aware field selection | rights/retention models | none | PIPA/GDPR profile review and E2E |
| Administration | FR-070–073 | versioned configuration and capability adapters | admin/provider contracts | none | item-level idempotency/replay tests |
| Tenant isolation | NFR security | Keyverse + RLS | auth context | none | adversarial cross-tenant suite |
| Availability | NFR reliability | operability and restore contracts | health/SLO/runbook | none | live telemetry and restore rehearsal |
| Page performance | NFR-010–013 | async long work; profile causal page path | k6 buyer-page evidence | none | realistic every-page p95 ≤ 20 ms |
| Accessibility | NFR-030–033 | WCAG 2.2 AA + Storybook | UX/design system | none | Figma, screenshots, AT audit |
| Internationalization | NFR-032 | DB-backed versioned resources; screen-key delivery | translation revision contract | none | ko/en/ja/zh/vi/es/de/fr Storybook/E2E |
| Scientific scoring | P-05 | Rust + TEPP/fast-mlsirm, no heuristics | model artifact/claim | none | validation study and model release gate |

## 4. Commercialization gap register

### G-001 Repository governance

**Owner:** ELUNVERA + organization control plane where causal.

**Current evidence:** `main` remains the canonical protected integration authority. The Draft foundation targets `main`; exact head `223228fd5ad8e37f6c5448ac6537dee9ae1c8598` had terminal GREEN document-contract, Security, and SAST runs, while CodeQL run `33889504891` was cancelled and qualifying approval remained absent when observed on 2026-10-01. Document-contract CI validates canonical branch authority and fails closed on performance/i18n contract drift.

**Gap:** exact-head required workflow completion, current semantic review, release-policy evidence, and any repository-specific ownership controls not centrally supplied remain unproven.

**Action:** preserve protected `main`, exact-head checks, independent review, and central reusable workflows; never weaken a leaf gate to compensate for hosted-runner or workflow-materialization failure.

**Exit evidence:** unchanged exact-head required checks plus ordinary protected integration.

### G-002 Executable production foundation

**Owner:** ELUNVERA.

**Current evidence:** a loopback Python/in-memory Activation Queue prototype plus static browser surface has complete local Python/browser test coverage on its source branch. It is not production architecture.

The carried prototype invariants are explicit: semantic `relationship_id` values are non-empty and unique within a snapshot set; buyer-visible party, kind, next-move, due, why-now, status, and optional provenance fields fail closed on malformed input; due values are real ISO dates; only known states are accepted; activated/dismissed relationships are terminal; HTTP actions must be strings; and one command mutates at most one aggregate. The loopback server serves only the product HTML/CSS/JavaScript and queue routes, so repository documents, workflows, dependency manifests, and arbitrary root paths remain outside the customer surface. The prototype now serializes competing writes with an in-process optimistic compare-and-set, so concurrent terminal commands cannot both succeed. Its loopback responses deny framing, and the UI distinguishes an accepted command from a later projection-refresh failure. RED head `16e583256b63e9c1f9208f6c322b6aa7e37a5381` reproduced the lost-update and framing failures in hosted product CI; successor `c7ee040df3e0dbf0e5bad6bf3f3dbfcade002454` implements the bounded repair. These remain in-memory/prototype controls, not durable tenant, cross-process concurrency, receipt, or release evidence.

**Gap:** no Rust workspace, tenant-aware production domain/API boundary, or durable adapter exists.

**Action:** preserve the prototype as bounded interaction evidence, then build the smallest Rust relationship-activation domain/API slice test-first rather than extending the Python adapter into production.

**Exit evidence:** Rust build/lint/unit/property/doc/coverage results on exact source.

### G-003 PostgreSQL lifecycle

**Owner:** ELUNVERA.

**Gap:** no migration, RLS, temporal constraint, pool, item-level UPSERT implementation, hot-lock evidence, backup, or restore.

**Action:** pin supported PostgreSQL 18.x, create 3NF multi-word persistence objects, RLS, temporal constraints, outbox, explicit item-level UPSERT/idempotency, contention tests, clean/upgrade rehearsal, encrypted backup, and restore validation.

**Exit evidence:** PostgreSQL integration, lock/contention, migration, backup, and restore artifacts.

### G-004 Keyverse integration

**Owner:** Keyverse for released identity contract; ELUNVERA for product-owned login/signup/recovery UI and ACL.

**Gap:** no OIDC/JWKS/SCIM implementation or product authentication forms.

**Action:** consume only immutable released Keyverse contracts; implement exact issuer/audience/token validation and immutable authorization context; keep CRM party identity distinct from authentication subject.

**Exit evidence:** negative token, tenant, recovery, CSS/action-edge, and integration tests.

### G-005 Account and relationship UX

**Owner:** ELUNVERA.

**Gap:** no Figma file, product-owned reusable component system, Storybook, production UI, screenshots, or accessibility evidence.

**Action:** create the three-band account experience in Figma, record file ID in ADR, implement design tokens/product-owned components and Storybook normal/loading/empty/error/permission/responsive/interaction states, then run full screenshot/E2E/AT audit.

**Exit evidence:** reviewed Figma, Storybook, screenshots, interaction tests, and WCAG evidence.

### G-006 Provider and CWL contracts

**Owner:** canonical supplier for reusable defects; ELUNVERA for consumer ACLs/adapters.

**Gap:** adapters and consumer contracts do not exist.

**Action:** consume only released immutable contracts. For an immature owner, use a port/ACL/feature flag/test double until owner RED→fix→GREEN→immutable release; never copy owner source, read owner DB, or bind to a temporary branch.

**Exit evidence:** supplier release plus consumer conformance, duplicate/reorder, outage, and reconciliation tests.

### G-007 Privacy operation

**Owner:** ELUNVERA.

**Gap:** purpose, rights, retention, hold, export, and disposition are documentation only.

**Action:** implement policy decision receipts and complete rights/disposition workflows before production PII; use least privilege, encryption, field selection, purpose limitation, and audit rather than destructive masking where masking breaks legitimate work.

**Exit evidence:** jurisdiction-reviewed policy plus realistic rights and non-masking-protection tests.

### G-008 Security and supply chain

**Owner:** `.github` for reusable controls; ELUNVERA for thin callers/product evidence.

**Gap:** the executable prototype has product CI, but no release artifact, production dependency inventory, SBOM/provenance/signature, penetration evidence, or production runtime exists.

**Action:** use released central workflows, exact pins, minimal permissions, fail-closed dependency/security gates, and signed release pipeline when runtime arrives.

**Exit evidence:** current-head checks, SBOM/provenance, signatures, and tested release candidate.

### G-009 Operability

**Owner:** ELUNVERA.

**Gap:** no health endpoints, telemetry, SLO, alert, capacity, incident, compose deployment, or recovery runtime.

**Action:** implement liveness/startup/readiness, async cancellation, OTLP, low-cardinality metrics, queue/backpressure, Compose for Docker/Podman/Colima, measured hardware tuning, runbooks, and recovery rehearsal. Verify `close_connection` assumptions in any framework/adapter before relying on them.

**Exit evidence:** SLO dashboard, realistic capacity run, and operational drill receipts.

### G-010 Model governance and measurement

**Owner:** ELUNVERA model domain plus released TEPP/fast-mlsirm/contextual-orchestrator contracts.

**Gap:** no model, dataset, benchmark, validity, fairness, or calibration evidence.

**Action:** release no score until outcome/population/sampling design/error target/failure denominator are defined; keep production numerical computation in Rust, model multilevel/multiple-membership/time structure where relevant, and prohibit heuristic weights.

**Exit evidence:** model card, true-parameter recovery/validation, calibration/error analysis, and monitoring.

### G-011 Commercial and legal readiness

**Owner:** ELUNVERA/product/legal.

**Current proposed slice:** Apache License 2.0 for ContextualWisdomLab-authored source/docs under Proposed ADR-0013.

**Gap:** no trademark evidence, terms, DPA, support policy, pricing, entitlement, billing integration, dependency/asset inventory, or sellable deployment.

**Action:** complete legal/commercial package only after protected foundation/runtime evidence.

**Exit evidence:** protected-main license/ADR integration plus reviewed commercial package and exact distributable SBOM/license/attribution evidence.

### G-012 Product validation

**Owner:** ELUNVERA product.

**Gap:** no customer interviews, usability data, activation, retention, willingness-to-pay, or outcome study.

**Action:** validate account-preparation, opportunity-review, and complaint-recovery jobs with target users and measure time-to-context, evidence coverage, correction rate, workflow outcome, and willingness-to-pay.

**Exit evidence:** research protocol and anonymized findings.

### G-013 Every-page performance contract

**Owner:** ELUNVERA.

**Evidence:** PRD/TRD/Test Strategy now require realistic every-buyer-page k6 p95 ≤ 20 ms; the permanent document-contract workflow prevents regression to weaker page targets.

**Gap:** only the loopback prototype runtime exists and it has no k6 buyer-page evidence, so no latency claim is proven.

**Action:** when the production UI/runtime starts, measure the full declared page denominator including DB/query/render/bundle/heap/DOM/hydration/main-thread/GC and cold/cache profile. Fix the causal algorithm/query/I/O/render/runtime/Rust hot path; never shrink data, omit slow samples, or use unrealistic warmup.

**Exit evidence:** exact-head k6 artifacts for every buyer-facing page at p95 ≤ 20 ms.

### G-014 Translation-resource authority and eight-locale delivery

**Owner:** ELUNVERA unless a separately released reusable CWL translation product later proves common ownership.

**Evidence:** PRD/TRD/UX/Test Strategy now specify `ko/en/ja/zh/vi/es/de/fr`, DB-backed versioned translation resources, screen-key-scoped server/native fetch/cache, review/approval/deploy/rollback, and separation from ontology labels.

**Gap:** no schema/API/admin UI/cache/locale assets or Figma/Storybook/E2E evidence exists.

**Action:** implement `translation_resource`, `translation_revision`, and `translation_text` in 3NF with immutable approved revisions, explicit draft item UPSERT, revision-aware cache invalidation, product-owned admin UI, and locale-specific interaction/screenshot tests.

**Exit evidence:** migration/API/admin UI + eight-locale Storybook/E2E + rollback and cache-invalidation receipts.

### G-015 Tracked-text hygiene

**Owner:** ELUNVERA.

**Evidence:** the previous exact-head document-contract workflow was GREEN even though a full PR-range `git diff --check` reported trailing whitespace in this baseline. The workflow's checkout-time `git diff --check` inspected only an empty working-tree diff.

**Gap:** formatting regressions in committed tracked text were not enforced by the permanent gate.

**Action:** validate every tracked non-binary file for trailing spaces or tabs, clean the current tree, and keep the check in the permanent document-contract workflow.

**Exit evidence:** the strengthened validator and full PR-range `git diff --check` both pass on the same exact head.

## 5. Highest-leverage implementation order

```text
canonical-main governance and foundation integration
→ reconcile stacked Relationship Activation delta without loss
→ identity and tenant boundary
→ PostgreSQL account/party/relationship kernel
→ audit, outbox, idempotency, temporal APIs
→ translation-resource authority + eight-locale component contract
→ three-band account UX + every-page k6 p95 ≤ 20 ms
→ opportunity and commitment vertical
→ complaints, outcomes, and privacy workflows
→ bounded released CWL integrations
→ validated relationship intelligence
→ scale, security, accessibility, recovery, and commercial GA
```

## 6. Release truth

This Draft documentation baseline fixes contradictory weak latency and two-locale requirements by making the current commercialization contract executable in document CI. It still closes none of the runtime, PostgreSQL, security, privacy, accessibility, model-validity, scalability, operational, broader legal/commercial, or market-validation gaps above. No release exists until an exact protected executable source and its required artifact, dependency, SBOM, provenance, review, performance, locale, accessibility, security, and operational evidence are independently established.
