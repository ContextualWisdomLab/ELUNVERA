# ELUNVERA Test Strategy

- **Document version:** 0.1
- **Status:** Proposed quality baseline
- **Date:** 2026-08-27

## 1. Objective

Testing must demonstrate product behavior, tenant and privacy boundaries, temporal correctness, scientific validity, accessibility, performance, recovery, and release reproducibility. Test counts or green status without realistic assertions are not sufficient evidence.

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

Validate domain state transitions, temporal interval operations, identifier handling, currency arithmetic, policy decisions, schema transformations, and error paths.

### Property tests

Generate sequences of commands and prove invariants including:

- no overlapping active role intervals where uniqueness is required;
- account merge plus reversal preserves all source references;
- debit-like exact amounts do not change under serialization round trips;
- idempotent command replay produces one event and one aggregate version;
- stage history never disappears after correction;
- disclosure decisions are monotonic with stricter policy;
- relationship participants remain tenant-consistent.

### Database integration tests

Run against real PostgreSQL 18.6 or a later supported 18.x patch. Validate migrations, RLS, temporal constraints, indexes, transaction isolation, outbox atomicity, lock behavior, partition pruning, backup, and restore.

### Contract tests

Validate OpenAPI, AsyncAPI, CloudEvents, JSON Schema, generated clients, Problem Details, pagination cursors, idempotency, ETags, provider adapters, and backward compatibility.

### Fuzz tests

Target parsers, identifiers, rich text, import payloads, webhook signatures, cursor decoding, date intervals, currency input, CSV/Office exports, and event envelopes.

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

### UX and accessibility tests

- keyboard-only journeys;
- screen-reader semantics;
- focus order and restoration;
- touch target and mobile viewport;
- high zoom and text reflow;
- reduced-motion preference;
- Korean and English copy expansion;
- loading, empty, partial, stale, conflict, denied, offline, and error states;
- exact-value tables and print/PDF output for charts;
- Storybook interaction and accessibility tests.

### End-to-end buyer journeys

1. Create an account, add stakeholders, record a relationship, and verify history.
2. Record an interaction and commitment, change status, and inspect evidence.
3. Progress an opportunity with optimistic concurrency and immutable stage history.
4. Receive a duplicate connector event and prove one canonical fact.
5. Resolve a complaint and connect remedy, outcome, and follow-up.
6. Submit a data-access case and inspect a purpose-limited export.
7. Attempt cross-tenant reads, writes, search, graph traversal, export, and model access.
8. Restore the system and prove data, outbox, projection, and key consistency.

## 4. Realistic fixtures

Fixtures represent multi-stakeholder B2B relationships, account hierarchy, role changes, former employees, multiple opportunities, delayed interactions, conflicting commitments, complaints, multiple currencies, duplicated events, malformed imports, and multilingual text. Names and organizations are synthetic.

Synthetic data is labeled and never used as evidence of customer accuracy or product-market fit.

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

A k6 or equivalent end-to-end suite exercises asynchronous and synchronous workflows. Initial engineering acceptance targets are:

| Workload | Target |
|---|---:|
| account summary read | p95 ≤ 300 ms at 200 concurrent users |
| account timeline, 1,000 entries | p95 ≤ 700 ms |
| relationship neighborhood, depth 2 | p95 ≤ 1.5 s with bounded result set |
| optimistic update | p95 ≤ 500 ms |
| event ingestion | sustained 1,000 events/s per deployment profile |
| queue admission under saturation | bounded response with no silent drop |
| export request | acknowledgement ≤ 500 ms; asynchronous completion |

These are release targets, not current performance claims. Tests record hardware, dataset size, connection pools, cache state, and commit SHA.

## 7. Recovery testing

- point-in-time restore into an isolated environment;
- active and predecessor key availability;
- schema compatibility and migration replay;
- outbox/inbox deduplication after restore;
- projection rebuild from canonical data;
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
Frontend lint, typecheck, unit, Storybook, and E2E
Coverage and documentation gate
SAST and secret scan
Dependency review and vulnerability scan
CodeQL or equivalent semantic analysis
Fuzz smoke and scheduled deep fuzz
Supply-chain SBOM and provenance
Production-readiness evidence
```

Every check runs on the exact PR head or merge-result tree specified by branch policy. Prior-head success is not current evidence.

## 9. Test-evidence manifest

A release manifest records command, environment, commit, dependency lock hash, database version, browser version, test counts, coverage denominators, skipped tests, benchmark profile, artifact hashes, and reviewer identity.
