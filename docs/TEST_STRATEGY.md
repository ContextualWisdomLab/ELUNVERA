# ELUNVERA Test Strategy

- **Document version:** 0.2
- **Status:** Proposed quality baseline
- **Date:** 2026-09-02

## 1. Objective

Testing must demonstrate product behavior, tenant and privacy boundaries, temporal correctness, scientific validity, accessibility, internationalization, performance, recovery, and release reproducibility. Test counts or green status without realistic assertions are not sufficient evidence.

## 2. Quality gates

For ELUNVERA-owned shipped code:

- production statement coverage: **100%**;
- production branch coverage: **100%**;
- public module, type, trait, function, method, error, and API documentation coverage: **100%**;
- skipped or ignored release tests: **0**, unless the release manifest explicitly excludes the feature;
- compiler and linter warnings: **0**;
- unresolved deprecation warnings: **0**;
- contract fixture failures: **0**.

Generated clients and third-party code are measured separately and may not dilute production coverage.

## 3. Test layers

### Unit tests

Validate domain state transitions, temporal interval operations, identifier handling, currency arithmetic, policy decisions, translation-resource revision transitions, schema transformations, and error paths.

### Property tests

Generate sequences of commands and prove invariants including:

- no overlapping active role intervals where uniqueness is required;
- account merge plus reversal preserves all source references;
- debit-like exact amounts do not change under serialization round trips;
- idempotent command replay produces one event and one aggregate version;
- stage history never disappears after correction;
- disclosure decisions are monotonic with stricter policy;
- relationship participants remain tenant-consistent;
- an approved translation revision is immutable and rollback selects a prior immutable revision;
- draft translation item UPSERT never creates duplicate `(translation_resource_id, locale_code, screen_key)` items within one revision.

### Database integration tests

Run against real PostgreSQL 18.6 or a later supported 18.x patch. Validate migrations, RLS, temporal constraints, indexes, transaction isolation, outbox atomicity, lock behavior, partition pruning, translation-resource item-level UPSERT/idempotency, backup, and restore.

### Contract tests

Validate OpenAPI, AsyncAPI, CloudEvents, JSON Schema, generated clients, Problem Details, pagination cursors, idempotency, ETags, provider adapters, translation screen-key/revision responses, and backward compatibility.

### Fuzz tests

Target parsers, identifiers, rich text, import payloads, webhook signatures, cursor decoding, date intervals, currency input, CSV/Office exports, translation keys/locale tags, and event envelopes.

### Security tests

Cover authentication, authorization, tenant isolation, purpose escalation, IDOR, injection, SSRF, path traversal, MIME confusion, formula injection, mass assignment, replay, privilege escalation, malicious redirects, and secret leakage.

### Model and scientific tests

A model feature cannot pass through ordinary snapshot tests alone. Required evidence includes:

- defined target outcome and population;
- gold or independently reviewed evidence set;
- true-parameter recovery for synthetic models where applicable;
- calibration and uncertainty evaluation;
- subgroup and context-specific error analysis;
- temporal validation and leakage-safe split;
- baseline and ablation comparisons;
- unsupported-claim rate;
- independent reviewer agreement;
- CPU/GPU parity for Rust numerical kernels;
- model/provider/prompt repeatability bounds.

Arbitrary weights and rule-of-thumb thresholds are prohibited.

### UX, accessibility, and locale tests

- keyboard-only journeys;
- screen-reader semantics;
- focus order, focus visibility, focus-not-obscured, and restoration;
- touch target and mobile viewport;
- high zoom and text reflow;
- reduced-motion preference;
- `ko/en/ja/zh/vi/es/de/fr` locale matrix covering CJK, expansion, wrapping, font fallback, dates, names, addresses, currencies, time zones, sorting, and validation copy;
- DB-backed translation revision fetch/cache/invalidation, review/approval/deploy/rollback, and no-full-browser-catalog assertions;
- loading, empty, partial, stale, conflict, denied, permission, offline, and error states;
- exact-value tables and print/PDF output for charts;
- Storybook interaction, locale, responsive, and accessibility tests;
- screenshot review for desktop, tablet, mobile, typography/color, forms/feedback, navigation, charts/data, and action edges.

### End-to-end buyer journeys

1. Create an account, add stakeholders, record a relationship, and verify history.
2. Record an interaction and commitment, change status, and inspect evidence.
3. Progress an opportunity with optimistic concurrency and immutable stage history.
4. Receive a duplicate connector event and prove one canonical fact.
5. Resolve a complaint and connect remedy, outcome, and follow-up.
6. Submit a data-access case and inspect a purpose-limited export.
7. Attempt cross-tenant reads, writes, search, graph traversal, export, and model access.
8. Restore the system and prove data, outbox, projection, translation revision, and key consistency.
9. Repeat buyer-visible journeys in every release locale with realistic expansion and CJK-sensitive content.

## 4. Realistic fixtures

Fixtures represent multi-stakeholder B2B relationships, account hierarchy, role changes, former employees, multiple opportunities, delayed interactions, conflicting commitments, complaints, multiple currencies, duplicated events, malformed imports, and multilingual text. Names and organizations are synthetic.

Synthetic data is unit-test-only and never used as evidence of customer accuracy, product-market fit, production load behavior, or buyer-facing latency.

## 5. Temporal validation

Tests use both business time and recorded time. Cases include:

- a later document describing an earlier event;
- a corrected stakeholder role;
- a backdated stage transition recorded today;
- a knowledge-cutoff query that must exclude later evidence;
- overlapping intervals rejected by constraint;
- daylight-saving and timezone boundaries;
- incomplete or uncertain intervals;
- merge and split history at different recorded times.

## 6. Performance and load

Realistic k6 end-to-end suites exercise every buyer-facing page and asynchronous workflow. Every buyer-facing page has a release target of **p95 ≤ 20 ms** at the declared ready-to-interact boundary under the documented release benchmark profile. The denominator includes all measured page samples; slow samples are not excluded, the dataset is not shrunk to pass, and warmup/cache state must reflect the declared production profile.

The harness records request, database/query, render, bundle/heap/DOM/hydration/main-thread/GC, network, connection-pool, and runtime evidence where applicable. If a page misses the target, the causal algorithm/query/I/O/render/runtime is profiled and repaired; sampling or thresholds are not weakened. Search or deep exploration that cannot fit the interactive budget becomes explicitly bounded/paginated or asynchronous.

Additional throughput and asynchronous contracts are:

| Workload | Target |
|---|---:|
| every buyer-facing page | p95 ≤ 20 ms |
| event ingestion | sustained 1,000 events/s per declared deployment profile |
| queue admission under saturation | bounded response with no silent drop |
| export/import/model/connector request | non-blocking acknowledgement with durable job status/cancellation |

Tests record hardware, CPU/GPU path when relevant, container limits, dataset size, PostgreSQL/app/shm configuration, connection pools, cache state, browser/runtime versions, and exact commit SHA. Docker, Podman, and Colima compatibility is exercised without using project-name overrides except for test isolation.

## 7. Recovery testing

- point-in-time restore into an isolated environment;
- active and predecessor key availability;
- schema compatibility and migration replay;
- outbox/inbox deduplication after restore;
- projection rebuild from canonical data;
- translation-resource revision and active-deployment restoration;
- object-store artifact reconciliation;
- lost worker and connection interruption;
- partial provider outage;
- rollback or forward-fix decision evidence.

## 8. CI structure

Suggested required checks:

```text
Contract and documentation validation
Rust format, lint, unit, property, and doc tests
PostgreSQL integration and migration rehearsal
Frontend lint, typecheck, unit, Storybook, locale, and E2E
k6 realistic buyer-page performance gate
Coverage and documentation gate
SAST and secret scan
Dependency review and vulnerability scan
CodeQL or equivalent semantic analysis
Fuzz smoke and scheduled deep fuzz
Supply-chain SBOM and provenance
Production-readiness evidence
```

Every check runs on the exact PR head or merge-result tree specified by branch policy. Prior-head success is not current evidence. A queued, skipped, startup-failed, or unmaterialized required job is not passing evidence.

## 9. Test-evidence manifest

A release manifest records command, environment, commit, dependency lock hash, database version, browser/runtime version, test counts, coverage denominators, skipped tests, locale matrix, benchmark profile, complete performance denominator, artifact hashes, and reviewer identity.
