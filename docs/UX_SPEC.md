# ELUNVERA UX Specification

- **Document version:** 0.2
- **Status:** Proposed interaction baseline
- **Date:** 2026-09-02

## 1. Experience objective

A customer-facing professional should understand an account, the people around it, what changed, what is at risk, and the next defensible action without reconstructing context from multiple applications.

The interface must expose evidence and uncertainty without turning the user into a graph-database operator or revealing internal CWL service boundaries.

## 2. Information architecture

```text
Home
Accounts
Relationships
Opportunities
Commitments
Complaints and Outcomes
Search
Reports
Administration
```

Email, calendar, files, projects, billing, and identity remain external products surfaced through integrated evidence or action references, not duplicated navigation hierarchies.

## 3. Account overview: three horizontal bands

The primary account page uses three full-width bands.

### Band 1 — Account context

- account identity, lifecycle, segment, owner, hierarchy, and current purpose;
- key customer outcomes and active commercial scope;
- last verified change and data freshness;
- compact actions: prepare interaction, add evidence, review duplicate.

### Band 2 — Relationship structure

- organization and stakeholder hierarchy;
- internal account team;
- time-valid roles and relationships;
- current, former, inferred, proposed, and disputed status;
- evidence and confidence drawer;
- exact-value/table alternative to any graph.

### Band 3 — Action and risk

- open commitments ordered by due state and consequence;
- opportunity decisions and unresolved assumptions;
- complaint recovery actions;
- recent changes requiring review;
- proposed next actions with evidence and human approval boundary.

The bands remain visible as an ordered vertical flow on smaller screens. They are not three equal dashboard cards.

## 4. Design principles

### Evidence near the claim

Every claim, stage change, recommendation, and score exposes source, recorded time, valid time, truth status, model status, and reviewer.

### Correct by exception

The product resolves routine context where evidence is sufficient and offers an obvious correction path. It avoids repeated disambiguation prompts but never hides uncertainty or performs irreversible action without approval.

### Next-action copy

Messages use customer language:

- “Review two conflicting stakeholder roles” rather than “relationship projection error.”
- “Reconnect the calendar source to update this commitment” rather than “naruon adapter unavailable.”
- “Refresh and compare changes before saving” rather than “optimistic lock exception.”

### Stable spatial memory

Navigation, filters, evidence drawers, and action placement remain consistent across accounts, opportunities, complaints, and commitments.

## 5. Core components

```text
AccountHeader
ContextBand
RelationshipBand
ActionBand
StakeholderTree
RelationshipGraph
RelationshipTable
Timeline
EvidenceDrawer
TruthStatusBadge
TemporalLens
CommitmentQueue
OpportunityStageHistory
ForecastEvidencePanel
ComplaintRecoveryPanel
OutcomeTracker
ModelClaimCard
ConflictResolutionPanel
DataRightsCasePanel
OperationReceipt
```

Each component has normal, loading, empty, partial, stale, access-denied, permission, conflict, offline, error, responsive, interaction, and completed states in Storybook before production acceptance.

## 6. Interaction rules

- No destructive action appears as a primary button without consequence preview.
- Stage transitions require effective time, reason, and evidence or explicit manual assertion.
- Account merge begins with a dry-run comparison and ends with a reversible receipt.
- Model proposals cannot be accepted through an unlabeled generic “Save.”
- Long jobs remain navigable after leaving the page.
- Filters and temporal lens are reflected in the URL without exposing restricted data.
- Back navigation restores scroll, selection, and expanded evidence state.
- Empty states explain required permission or next action.

## 7. Search experience

Search accepts business language and structured filters. Results show:

- why the item matched;
- authority and truth status;
- effective and recorded time;
- account and relationship context;
- access-limited field omissions;
- source evidence;
- the action available from the result.

A generative answer is accompanied by a result set and claim-by-claim evidence. Search never fabricates a missing fact to produce fluent prose.

## 8. Accessibility

Target: WCAG 2.2 AA.

- all workflows keyboard operable;
- visible focus and logical order;
- no color-only truth or risk state;
- graph has structured table and text summary;
- charts provide exact-value table and export;
- 200% zoom without two-dimensional scrolling for ordinary content;
- touch targets meet target-size guidance;
- motion respects reduced-motion preference;
- live regions are limited and non-disruptive;
- drag-and-drop has button and keyboard alternatives;
- errors identify the field, cause, and recovery action.

## 9. Internationalization and translation authority

Korean, English, Japanese, Chinese, Vietnamese, Spanish, German, and French are first-release interface languages. Copy is not concatenated from fragments. Dates, names, addresses, currencies, time zones, honorifics, organization order, font fallback, CJK behavior, and text expansion are locale-aware. The canonical data model does not assume Western given-name or organization formats.

Translation authority uses DB-backed, versioned translation resources with explicit draft, review, approval, deployment, rollback, and immutable revision history. Server/native delivery fetches and caches only screen-scoped keys and revisions. The browser does not receive the full translation catalog and does not require a heavyweight i18n runtime. Product UI copy and ontology labels are separate responsibilities.

Figma and Storybook must exercise every supported locale at expansion-prone and CJK-sensitive sizes, including navigation, forms, validation, empty/error/permission states, charts/tables, modals, destructive confirmation, and mobile action edges.

## 10. Responsive behavior

- desktop: persistent navigation, three-band account flow, evidence drawer;
- tablet: collapsible navigation and contextual side sheet;
- mobile: single-column bands, bottom action sheet, compact temporal controls;
- print/PDF: account brief with evidence references and no hover dependence.

## 11. Design system and Figma

A Figma file is required before implementation of the production interface. Its file ID is recorded in an ADR once created. Design tokens are source-controlled and shared with Storybook. The Figma library must cover account overview, relationship exploration, opportunity review, complaint recovery, exports, all edge states, all eight release locales, keyboard focus, touch interactions, responsive layouts, and print.

shadcn/ui, when selected, is imported as product-owned component source rather than treated as an external runtime design authority. Reusable components are validated in Storybook before page composition.

## 12. UX validation

- task-based usability testing with account executives, account managers, customer-success users, operations administrators, and privacy/security reviewers;
- accessibility audit with automated and assistive-technology testing;
- screenshot review at desktop, tablet, and mobile breakpoints across all eight release locales;
- keyboard, touch, focus-not-obscured, responsive, typography/color, reduced-motion, forms/feedback, navigation, charts/data, and action-edge audits;
- realistic k6 page journeys with p95 ≤ 20 ms at the ready-to-interact boundary; slow samples and rendering/main-thread costs are retained in the denominator;
- copy review ensuring customer action language and absence of internal implementation boundaries;
- event instrumentation reviewed for privacy and semantic consistency.
