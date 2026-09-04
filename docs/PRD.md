# ELUNVERA Product Requirements Document

- **Document version:** 0.2
- **Status:** Proposed product baseline
- **Date:** 2026-09-02
- **Product:** ELUNVERA
- **Repository:** `ContextualWisdomLab/ELUNVERA`
- **Primary branch:** `main`

## 1. Executive summary

ELUNVERA is an evidence-centered enterprise CRM and relationship-intelligence platform. It is designed for organizations whose customer context is fragmented across email, meetings, documents, account plans, opportunity records, support cases, customer feedback, and the memory of individual employees.

The product converts that scattered context into a governed customer relationship record, a time-valid account and stakeholder model, and a prioritized queue of evidence-linked actions. Human judgment remains authoritative. ELUNVERA may propose interpretations, risks, and next actions, but it does not silently send messages, change opportunity stages, close cases, or disclose customer information.

## 2. Product vision

> Help every customer-facing team understand the relationship as it actually exists, see what changed, and take the next defensible action with evidence.

ELUNVERA broadens CRM beyond a contact database or sales pipeline. Its five cross-functional product processes are:

1. relationship and account strategy;
2. value and outcome definition;
3. multichannel interaction integration;
4. governed information and evidence management;
5. performance, satisfaction, and relationship assessment.

These processes align with the strategic, cross-functional view of CRM described by Payne and Frow rather than treating CRM as a sales-force data-entry tool.

## 3. Problem statement

Customer-facing teams currently experience the following failures:

- account and stakeholder truth is duplicated across spreadsheets, inboxes, chat, and individual notes;
- organizational and interpersonal roles change over time but records are overwritten;
- a meeting, email thread, complaint, contract discussion, and delivery issue are not connected into one decision context;
- opportunity stages and probabilities are often based on local convention rather than calibrated evidence;
- a new account owner cannot reconstruct commitments and stakeholder history;
- important customer facts are exposed too broadly or hidden by destructive masking;
- generic AI summaries omit provenance, uncertainty, and the next action;
- customer satisfaction and relationship “health” are reduced to opaque weighted scores;
- integrations copy source data without a stable authority, idempotency, or deletion contract.

## 4. Product principles

### P-01 Relationship truth is temporal

Roles, affiliations, account status, stakeholder participation, ownership, and disclosure policy change over time. ELUNVERA preserves historical truth instead of overwriting it.

### P-02 Evidence precedes inference

A relationship, commitment, risk, or recommendation must link to source evidence or explicitly declare that it is manually asserted. Inferred claims never become authoritative facts automatically.

### P-03 Human judgment remains authoritative

The product reduces cognitive load and proposes a defensible next action. It does not replace customer-facing judgment or authority.

### P-04 Context is purpose-bound

Authorized operational users may need unmasked customer information. ELUNVERA protects that information through purpose limitation, field selection, least privilege, disclosure policy, encryption, and audit rather than making the system unusable through universal masking.

### P-05 No arbitrary commercial scoring

Forecast probability, relationship health, stakeholder influence, lead score, and churn risk may not be computed from undocumented weights or stage defaults. A score requires a versioned model, defined outcome, calibration evidence, uncertainty, and monitoring.

### P-06 Federated products retain their own truth

ELUNVERA integrates with other CWL products without copying their authority or implementation.

### P-07 Customer copy supports the next action

Every alert, empty state, error, and AI response explains what happened, why it matters, and the available next action without exposing internal service names.

## 5. Target customers

### Primary segments

- B2B organizations with complex, multi-person accounts;
- enterprise sales and account-management teams;
- customer-success and renewal teams;
- professional-services and solution-delivery organizations;
- regulated organizations that require data lineage, auditability, and purpose-aware access.

### Initial deployment profile

The first commercial profile is a multi-tenant or customer-isolated enterprise SaaS deployment for Korean and international B2B account teams. Korean, English, Japanese, Chinese, Vietnamese, Spanish, German, and French ship as first-release interface locales, with optional customer-controlled connectors.

## 6. Personas

| Persona | Primary job | Critical concern |
|---|---|---|
| Account executive | Progress an opportunity with accurate stakeholder and commitment context | Avoid stale or invented deal confidence |
| Account manager | Preserve and grow a long-term commercial relationship | Understand role changes and customer outcomes |
| Customer success manager | Coordinate adoption, risk, complaint, and renewal activity | Separate observed signals from inferred risk |
| Sales manager | Review pipeline and coach account teams | See evidence and forecast uncertainty, not only totals |
| Revenue operations analyst | Govern stages, taxonomies, data quality, and forecast processes | Versioned processes and reproducible metrics |
| Customer-service lead | Handle complaints and service recovery | ISO-aligned complaint history and closure evidence |
| Privacy or security officer | Control customer-data use and disclosure | Purpose, retention, access, export, and incident evidence |
| Executive | Understand material relationship changes and commercial exposure | Concise, exact, drillable information |
| Platform administrator | Configure tenants, roles, integrations, and policies | Fail-closed isolation and operability |

## 7. Core jobs to be done

### JTBD-01 Prepare for a customer interaction

When a customer meeting is approaching, assemble the current account context, recent changes, open commitments, stakeholder roles, prior decisions, and unresolved risks with evidence so the user can prepare without searching multiple systems.

### JTBD-02 Understand an account

When ownership changes or an issue arises, show the organization hierarchy, account roles, people, relationship history, products or services in context, and current outcomes without flattening them into one score.

### JTBD-03 Progress a commercial opportunity

When a team updates an opportunity, preserve the stage transition, evidence, stakeholders, criteria, values, assumptions, and forecast snapshot so later reviews can reproduce why the change occurred.

### JTBD-04 Protect commitments

When a customer or team member makes a commitment, track the authoritative status, owner, due interval, evidence, and downstream action without converting email content into an unreviewed task automatically.

### JTBD-05 Recover service and complaints

When a customer reports a complaint, preserve receipt, classification, ownership, communication, remedy, response, verification, and closure evidence.

### JTBD-06 Measure outcomes responsibly

When leaders need a customer or relationship assessment, use versioned instruments and calibrated models, report uncertainty and population limits, and retain evidence from observation through decision.

### JTBD-07 Exercise data rights

When a person requests access, export, correction, restriction, or deletion, identify all relevant authoritative and projected data, execute a policy-controlled workflow, and preserve a receipt without deleting protected audit or legal-hold facts.

## 8. Product scope

### 8.1 P0 — Foundation

- tenant and workspace configuration;
- Keyverse identity integration and role mapping;
- commercial account registry;
- party registry for people, organizations, and groups;
- time-valid account and party roles;
- first-class relationship facts with evidence and disclosure policy;
- account-team assignments;
- contact points and purpose-specific communication preferences;
- manual interactions, notes, evidence references, and commitments;
- opportunity registry, configurable stage definitions, stage history, stakeholders, values, products or offerings by reference, and forecast snapshots;
- immutable audit and transactional outbox;
- deterministic CSV/JSON import and export;
- account search and duplicate-candidate workflow;
- Korean, English, Japanese, Chinese, Vietnamese, Spanish, German, and French interface baseline;
- DB-backed, versioned translation resources with review, approval, deployment, rollback, and screen-key-scoped delivery;
- account overview, relationship map, timeline, opportunity workspace, and action queue.

### 8.2 P1 — Integrated context

- naruon interaction metadata and source references;
- ThreadWeave thread references;
- LineageWeave inferred-lineage proposals;
- ScopeWeave work-item references;
- Semantic Data Portal ontology links;
- RankWeave retrieval fusion;
- evidence-grounded account and meeting briefs through contextual-orchestrator;
- customer complaint workflow aligned to ISO 10002;
- satisfaction observation and monitoring workflow aligned to ISO 10004;
- customer outcome and renewal context;
- controlled data-rights workflow;
- administrative data-quality console.

### 8.3 P2 — Calibrated relationship intelligence

- TEPP temporal event and relationship analysis;
- fast-mlsirm calibration for LLM-as-a-judge or rater-like assessments;
- model registry, population scope, true-parameter recovery evidence, drift monitoring, and uncertainty;
- account health and opportunity risk as evidence-based model artifacts;
- forecast calibration and outcome analysis;
- explainable intervention recommendations;
- opt-in Figma-validated advanced graph and temporal visual analytics.

## 9. Explicit non-goals

ELUNVERA will not initially:

- host mailboxes, SMTP, IMAP, CalDAV, or WebDAV;
- provide full marketing automation, ad targeting, or campaign execution;
- replace ERP, CPQ, contract lifecycle, order management, accounting, or billing systems;
- replace ScopeWeave for project, WBS, ITSM, or generalized work management;
- replace Orgmetra for employee and employment truth;
- replace the Semantic Data Portal as an enterprise ontology and catalog;
- copy raw external-system data without source authority and retention contracts;
- derive high-stakes customer or employee decisions from a single LLM response;
- claim compliance certification merely because controls are documented.

## 10. Functional requirements

### Account and party management

- **FR-001:** The system shall create and version tenant-scoped commercial accounts.
- **FR-002:** The system shall represent people, organizations, and groups as separate party types under a canonical party identity.
- **FR-003:** The system shall preserve organization hierarchy and merger, subsidiary, partner, customer, prospect, and former-customer roles as time-valid relations rather than immutable entity types.
- **FR-004:** The system shall support duplicate candidates, review, merge, split, and merge reversal with provenance.
- **FR-005:** The system shall never use an email address as the permanent identity of a person or account.

### Relationships and stakeholders

- **FR-010:** A relationship shall include participants, type, context, valid interval, truth status, evidence, confidence when inferred, source authority, and disclosure policy.
- **FR-011:** The same parties may have multiple simultaneous relationships in different contexts.
- **FR-012:** Opportunity and account stakeholder roles shall be versioned and organization-configurable.
- **FR-013:** The system shall distinguish manually asserted, observed, inferred, proposed, rejected, and superseded relationship facts.

### Interactions and commitments

- **FR-020:** The system shall record interactions without requiring raw message bodies.
- **FR-021:** External interaction references shall identify source system, immutable source key, captured time, and source hash or receipt when available.
- **FR-022:** A commitment shall include status, owner, beneficiary, valid/due interval, evidence, and completion or supersession history.
- **FR-023:** Imported interaction and commitment items shall be idempotent at item level.
- **FR-024:** AI-extracted commitments shall remain proposed until accepted by an authorized user or an approved deterministic rule.

### Opportunities and forecasts

- **FR-030:** Sales processes and stage definitions shall be versioned by tenant or workspace.
- **FR-031:** Stage transitions shall be append-only and include actor, reason, evidence, business time, and recorded time.
- **FR-032:** Monetary values shall use exact decimal quantities and explicit ISO 4217 currency codes.
- **FR-033:** Forecast snapshots shall be immutable and distinguish user category, manager adjustment, and model estimate.
- **FR-034:** Model estimates shall include model version, training/evaluation population, estimate interval, calibration evidence, and knowledge cutoff.
- **FR-035:** The system shall not infer forecast probability from stage alone.

### Customer outcome and complaint management

- **FR-040:** The system shall record desired customer outcomes, observation periods, measures, and evidence.
- **FR-041:** Complaint handling shall preserve receipt, acknowledgement, classification, owner, investigation, response, remedy, verification, escalation, and closure.
- **FR-042:** Satisfaction observations shall reference an instrument or defined measurement procedure and population.
- **FR-043:** Customer health assessments shall expose contributing evidence and uncertainty and may abstain.

### Search and intelligence

- **FR-050:** Search results shall preserve channel contribution, source, and access decision.
- **FR-051:** AI briefs shall cite ELUNVERA evidence references and distinguish facts, inferences, unknowns, and recommended actions.
- **FR-052:** The assistant shall not disclose data outside the user’s purpose, tenant, role, field, and relationship-disclosure policy.
- **FR-053:** Irreversible or external actions shall require an explicit human approval or a separately approved automation policy.

### Privacy, security, and data rights

- **FR-060:** Every request shall carry verified tenant, actor, role, purpose, and correlation context.
- **FR-061:** Contact and relationship fields shall support purpose-specific access and export rules.
- **FR-062:** The system shall support access, export, correction, restriction, retention, legal hold, and deletion workflows with receipts.
- **FR-063:** Audit, legal-hold, transaction, and historical relationship facts shall not be silently deleted.
- **FR-064:** Event payloads shall use opaque references and exclude secrets and unnecessary raw PII.

### Administration and integration

- **FR-070:** Administrators shall configure role taxonomies, sales processes, field policies, retention profiles, integration capabilities, and model permissions through versioned configuration.
- **FR-071:** External systems shall connect through capability-specific adapters, not one lowest-common-denominator integration interface.
- **FR-072:** Every provider command and webhook shall be idempotent, signed or authenticated, replay-protected, and recorded.
- **FR-073:** The system shall retain a provider-object mapping rather than adding provider-specific IDs to core domain tables.

## 11. Non-functional requirements

### Availability and reliability

- **NFR-001:** Initial GA target is 99.9% monthly availability for authenticated API and web workflows, excluding announced maintenance.
- **NFR-002:** Accepted writes shall be durable before success is returned.
- **NFR-003:** Outbox publication shall be retryable and at-least-once; consumers shall be idempotent.
- **NFR-004:** Backup and point-in-time restoration shall be rehearsed before release.

### Performance

- **NFR-010:** Every buyer-facing page shall achieve realistic end-to-end p95 ≤ 20 ms under the declared release benchmark profile. The measurement must include the page request, product-owned data access, rendering, and ready-to-interact boundary; it may not be met by shrinking datasets, excluding slow samples, or using an unrealistic warmup. Long-running AI or connector work remains an explicit asynchronous job and may not block page readiness.
- **NFR-011:** Search-backed pages are subject to the same p95 ≤ 20 ms page target. Deep or unbounded exploration that cannot satisfy the interactive budget shall be paginated or moved to an explicit asynchronous workflow rather than weakening the page SLO.
- **NFR-012:** Long-running exports, imports, model runs, and connector synchronizations shall use durable asynchronous jobs with status and cancellation.
- **NFR-013:** Product UI shall never wait synchronously for an LLM workflow to complete.

### Scale baseline

The first release benchmark shall cover:

- 1,000 tenants;
- 1,000,000 commercial accounts;
- 20,000,000 parties;
- 100,000,000 interactions;
- 10,000,000 relationships;
- 5,000,000 opportunities;
- concurrent ingestion and read traffic with noisy-tenant controls.

These are acceptance targets, not current performance claims.

### Security and privacy

- **NFR-020:** Cross-tenant access acceptance target is zero successful accesses across API, database, cache, search, export, and background jobs.
- **NFR-021:** All external data and model output shall be treated as untrusted input.
- **NFR-022:** Encryption in transit and at rest shall be mandatory for production.
- **NFR-023:** Customer-content logging shall be disabled by default.
- **NFR-024:** Security and privacy controls shall support ISO/IEC 27001:2022, ISO/IEC 27701:2025, SOC 2, CSAP, Korean PIPA, and GDPR deployment evidence without claiming certification.

### Accessibility and internationalization

- **NFR-030:** Web experiences shall conform to WCAG 2.2 AA.
- **NFR-031:** Every graph, chart, and timeline shall have an exact-value table and export representation.
- **NFR-032:** Korean, English, Japanese, Chinese, Vietnamese, Spanish, German, and French shall ship together, with locale-safe dates, names, addresses, number formats, sorting, font fallback, CJK behavior, and expansion-safe layouts. Translation authority shall use DB-backed, versioned translation resources with review, approval, deployment, and rollback; server/native clients fetch and cache only screen-scoped keys rather than downloading a full browser catalog.
- **NFR-033:** Customer-facing copy shall describe the user’s next action rather than internal implementation boundaries.

### Quality

- **NFR-040:** ELUNVERA-owned shipped code shall have 100% production statement coverage, 100% production branch coverage, and 100% public API documentation coverage.
- **NFR-041:** Required GPU tests may not pass by being skipped.
- **NFR-042:** Deprecation warnings shall be corrected, not suppressed.
- **NFR-043:** Release artifacts shall include SBOM, provenance, signatures, compatibility metadata, and reproducible-build evidence.

## 12. Primary user journeys

### Journey A — Account preparation

1. User opens the account judgment queue.
2. ELUNVERA shows changes since the user’s last verified view.
3. User opens an account overview with three bands: context, relationships, and action.
4. Recent interactions, open commitments, stage changes, customer outcomes, and unresolved evidence conflicts are visible.
5. The evidence-grounded assistant proposes a meeting brief and next actions.
6. User accepts, edits, or rejects each proposed action independently.

### Journey B — Opportunity review

1. Manager opens the opportunity workspace.
2. Current stage, complete stage history, stakeholder evidence, value snapshots, assumptions, and forecast sources are visible.
3. A model estimate is shown only when model release criteria are satisfied; otherwise the system abstains.
4. Manager records a review decision and reason without overwriting the prior forecast.

### Journey C — Complaint recovery

1. A complaint arrives through manual entry or a controlled connector.
2. ELUNVERA acknowledges receipt and records the source.
3. An owner investigates and links evidence, affected products, interactions, and commitments.
4. Response and remedy are approved and communicated through the source system.
5. Verification and closure are recorded; satisfaction follow-up is scheduled if permitted.

## 13. Product success measures

Success measures shall be segmented by tenant, account complexity, role, and adoption cohort. A metric is not a product goal merely because it is easy to count.

| Dimension | Measure |
|---|---|
| Context efficiency | Median time from account open to evidence-backed action decision |
| Continuity | Proportion of active accounts with current ownership, stakeholder, and commitment context |
| Data quality | Duplicate rate, stale-role rate, unresolved identity rate, source-receipt completeness |
| Action reliability | Accepted commitments completed on time; proposed actions accepted, edited, or rejected |
| Forecast quality | Calibration error, interval coverage, bias, and drift by segment |
| Relationship measurement | Reliability, validity, invariance, and uncertainty of released instruments/models |
| Customer outcome | Complaint cycle time, verified closure, recurrence, and satisfaction follow-up |
| Trust | Unauthorized access attempts blocked, data-rights completion, export provenance completeness |
| Operability | Availability, latency, job recovery, restore success, and incident recurrence |
| Accessibility | Automated and manual WCAG conformance and assistive-technology journey success |

## 14. Release acceptance

A first production release may be proposed only when:

- the P0 vertical operates end to end on a clean deployment;
- current-head tests and security checks pass;
- tenant isolation is proven at API and database layers;
- migrations, rollback, backup, and restore are rehearsed;
- exact user journeys pass in Korean, English, Japanese, Chinese, Vietnamese, Spanish, German, and French;
- every buyer-facing page meets the declared realistic k6 p95 ≤ 20 ms release profile without excluded slow samples or synthetic production traffic;
- translation-resource review, approval, cache invalidation, deployment, and rollback are exercised against DB-backed versioned resources;
- accessibility journeys pass with keyboard and screen-reader evidence;
- no critical or high unaccepted security finding remains;
- every numerical model in the release has documented validation and uncertainty;
- documentation and observed implementation state are consistent;
- signed artifacts, SBOM, provenance, runbooks, and changelog are complete.

## 15. Assumptions and open implementation decisions

This baseline intentionally decides the product boundary and quality contract but does not claim that a runtime exists. Implementation details such as exact web framework versions, message transport, object-storage provider, deployment platform, and first customer-specific connectors must be selected through reviewed ADRs when executable work begins.
