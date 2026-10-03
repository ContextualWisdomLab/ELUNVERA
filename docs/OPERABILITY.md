# ELUNVERA Operability Baseline

- **Document version:** 0.1
- **Status:** Proposed operational baseline
- **Date:** 2026-08-27

## 1. Operating objective

Operate ELUNVERA as a recoverable, observable, tenant-isolated customer system of record. Operational health means not only process liveness but the ability to authenticate, commit canonical writes, publish events, execute bounded jobs, protect data, and restore service.

## 2. Runtime profiles

### Development

Compose-compatible local profile using Podman, Colima, or Docker; ephemeral synthetic data; no production credentials.

### Single-customer isolated deployment

Dedicated application, database, object storage, and Keyverse realm or tenant mapping. Suitable for regulated or data-sovereign customers.

### Multi-tenant SaaS

Shared control plane with database-enforced isolation, fair scheduling, tenant-aware capacity, and regional deployment policy.

All profiles use the same contracts and migration history.

## 3. Health endpoints

| Endpoint | Meaning | Dependency checks |
|---|---|---|
| `/healthz` | process liveness | event loop and internal watchdog only |
| `/startupz` | startup completion | configuration, contract version, migrations |
| `/readyz` | safe to receive traffic | DB read/write path, key availability, queue admission, required policy |

An optional provider outage does not fail core readiness unless the requested profile marks that provider as mandatory. Readiness output is bounded and exposes no secret or internal topology.

## 4. Service-level objectives

Initial GA targets:

- authenticated core API availability: 99.9% monthly;
- accepted canonical writes durability: 99.999% excluding declared disaster scenarios;
- p95 core read latency: 500 ms for documented baseline workload;
- p95 core write latency: 750 ms;
- outbox publication lag: 99% under 60 seconds;
- customer-visible job start lag: 99% under 2 minutes under contracted capacity;
- restoration point objective: 15 minutes;
- restoration time objective: 4 hours for the initial profile.

SLOs are measured over low-cardinality signals and accompanied by multi-window burn-rate alerts.

## 5. Telemetry

### Metrics

- request count, latency, result class, and route template;
- authorization outcome by policy code, not personal identity;
- DB pool use, wait, transaction duration, lock wait, and rollback;
- outbox/inbox lag, retries, dead letters, and deduplication;
- job queue depth, age, execution, cancellation, and failure code;
- object-storage and export outcomes;
- connector latency, circuit state, and bounded error category;
- model job cost/usage references without prompt content;
- tenant resource quota and saturation using opaque tenant labels where permitted.

### Traces

Traces propagate correlation and causation IDs across domain, outbox, worker, and adapter boundaries. They exclude raw notes, messages, names, contact details, access tokens, and unrestricted tenant identifiers.

### Logs

Structured events use stable error codes. No stack trace is returned to a customer. Sensitive diagnostic logs require time-bound privileged access and retention.

## 6. Capacity management

Capacity models include tenant count, account count, relationship count, interaction volume, outbox volume, timeline query depth, export volume, job concurrency, and projection size. Autoscaling is not a substitute for bounded work.

Connection pools and Rust worker pools are fixed from measured capacity. External libraries must not create uncontrolled nested pools or thread oversubscription.

## 7. Backpressure

- synchronous paths reject oversized or over-budget work before allocation;
- queues use bounded admission and tenant fairness;
- workers lease jobs with heartbeat and safe recovery;
- retries are bounded and preserve idempotency;
- optional model or provider work degrades to an explicit unavailable state;
- core account and opportunity writes do not depend on an LLM.

## 8. Backup and restoration

- encrypted base backup plus WAL or equivalent point-in-time recovery;
- object-storage versioning and retention policy;
- key and configuration backup with separate access controls;
- schema and release manifest stored with each backup series;
- scheduled restoration into an isolated environment;
- record-count, hash, temporal, RLS, outbox, object, and projection checks after restore;
- documented evidence and remediation for every rehearsal.

A backup that has not been restored successfully is not accepted as recovery evidence.

## 9. Migration operation

Migrations use expand, backfill, verify, and contract phases. The runtime fails closed if schema is ahead or behind the supported compatibility window. Long backfills are resumable, tenant-bounded, observable, and do not hold unbounded locks.

Migration rehearsals cover clean install and upgrade from the previous supported release. Rollback feasibility is declared per migration; irreversible migrations require restore or forward-fix procedures.

## 10. Incident response

Severity classification considers customer impact, confidentiality, integrity, availability, legal obligation, and commercial consequences. Runbooks cover:

- authentication or tenant-isolation failure;
- data corruption or erroneous merge;
- connector duplication;
- key loss or rotation failure;
- model/provider data exposure;
- queue saturation;
- database failover and restore;
- supply-chain compromise;
- privacy request breach;
- export to an unauthorized recipient.

Incident evidence may feed the GRC product but ELUNVERA remains the source for its operational audit facts.

## 11. Administrative safety

- no routine operation through direct database edits;
- all privileged commands have dry-run where feasible;
- bulk and destructive actions require receipts and approval;
- emergency access is time-limited, purpose-bound, and alerted;
- support impersonation is disabled or implemented as explicit delegated view with a persistent banner and audit record;
- maintenance mode distinguishes read-only from unavailable.

## 12. Release and rollback

A release includes signed OCI image, SBOM, provenance, migrations, contract compatibility report, test evidence, known limitations, rollback coordinates, and CHANGELOG. Promotion uses the same artifact digest across environments.

Rollback never rewrites history. If the database has crossed an irreversible boundary, the release plan specifies forward fix or restore rather than claiming binary rollback.

## 13. Operational readiness gate

No production deployment until:

- core SLO signals and paging are live;
- on-call ownership and escalation exist;
- clean install and upgrade rehearsal pass;
- backup and restoration evidence passes;
- tenant isolation and security checks pass;
- capacity baseline and limits are documented;
- incident and data-rights runbooks are reviewed;
- support can identify the current release and contract versions;
- known residual risks have owners and expiration dates.
