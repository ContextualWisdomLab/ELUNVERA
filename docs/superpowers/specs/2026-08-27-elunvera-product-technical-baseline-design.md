# ELUNVERA Product and Technical Baseline Design

- **Date:** 2026-08-27
- **Status:** Proposed
- **Scope:** Documentation and executable-contract design; no runtime implementation

## 1. Intent

Establish a coherent design baseline for a new evidence-centered B2B CRM that can enter implementation through canonical protected `main` without absorbing adjacent CWL products or inventing unvalidated commercial scores.

## 2. Considered approaches

### Full-suite CRM monolith

Own identity, email, calendar, projects, billing, content, and intelligence in one repository. This offers a superficially simple sales story but duplicates CWL authorities and creates a large regulatory and operational blast radius. Rejected.

### Graph-only relationship overlay

Project existing customer systems into a graph and provide search/AI. This avoids another transactional store but cannot own stage history, commitments, complaint workflow, privacy rights, or accountable corrections. Rejected as the core product.

### Federated CRM system of record with evidence-centered intelligence

Own the customer relationship and commercial facts that require transactional authority. Consume adjacent capabilities through bounded contracts. Preserve first-class bitemporal relationships and separate model claims from facts. **Selected.**

## 3. Product boundary

ELUNVERA owns account, party, relationship, interaction metadata, commitment, opportunity, outcome, complaint, satisfaction observation, purpose, preference, rights workflow, audit, and provenance facts. Keyverse, naruon, ThreadWeave, LineageWeave, RankWeave, contextual-orchestrator, TEPP, fast-mlsirm, Semantic Data Portal, ScopeWeave, and Billing Control Plane retain their own authorities.

## 4. Architecture

The first implementation is a Rust modular monolith with PostgreSQL 18 as canonical store, transactional outbox, durable worker, rebuildable search/graph projections, and Next.js/TypeScript interfaces. Module contracts make later service extraction possible without requiring distributed transactions at inception.

## 5. Data design

- 3NF canonical records;
- UUIDv7 external identifiers;
- RLS or equivalent database tenant isolation;
- business-valid and system-recorded time;
- first-class n-ary relationship records;
- exact decimal money;
- external-provider IDs in mapping tables;
- immutable audit, stage, forecast, model, and disposition evidence;
- graph/search/vector as projections only.

## 6. Command and event flow

Mutations require verified identity context, purpose, idempotency key, and current aggregate version. Aggregate and outbox event commit atomically. Events use CloudEvents with versioned JSON Schema and at-least-once delivery; consumers deduplicate and record projection receipts.

## 7. AI and measurement

LLM work runs through contextual-orchestrator and produces model claims with evidence and uncertainty. A separate authorized command changes domain truth. Scores require construct and outcome definition, validation population, temporal and multilevel design, calibration, fairness, uncertainty, and release monitoring. Heuristic stage probabilities and weighted health scores are forbidden.

## 8. UX

The account overview follows three horizontal bands: account context, relationship structure, and action/risk. Graphs always have exact structured alternatives. Copy explains the customer’s next action and hides internal component names. Figma, design tokens, Storybook, Korean/English, responsive states, screenshots, and WCAG 2.2 AA evidence precede UI completion.

## 9. Failure behavior

Core CRM reads and writes do not depend on optional providers or LLMs. Integration failure produces an explicit stale/partial state and recovery action. Expensive operations are asynchronous, bounded, cancellable, and receipted. Restore, projection rebuild, duplicate/reorder, and provider-outage cases are first-class tests.

## 10. Quality boundary

ELUNVERA-owned shipped code requires 100% production statement and branch coverage and 100% public API documentation. Current-head checks, realistic PostgreSQL, security, accessibility, load, migration, recovery, SBOM, provenance, and independent review are release gates.

## 11. Scope decision

This specification is focused enough for one foundation implementation plan because the plan delivers a usable canonical account/relationship vertical. Later opportunity, complaint, integration, and intelligence milestones receive separate implementation plans.
