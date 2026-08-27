# ELUNVERA Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the first executable ELUNVERA vertical: authenticated tenant-isolated accounts, parties, time-valid relationships, evidence references, immutable audit, and a three-band account read model.

**Architecture:** A Rust modular monolith exposes OpenAPI-derived HTTP contracts over a PostgreSQL 18 canonical store. Writes use idempotency, optimistic concurrency, RLS, temporal constraints, and a transactional outbox; a worker builds a read model consumed by a Next.js interface.

**Tech Stack:** Rust stable, Axum, Tokio, SQLx, PostgreSQL 18.6+, OpenAPI 3.2.0, JSON Schema 2020-12, Next.js/React/TypeScript, OpenTelemetry, cargo-nextest, cargo-llvm-cov, proptest, cargo-fuzz, Playwright, Storybook.

**Spec:** `docs/superpowers/specs/2026-08-27-elunvera-product-technical-baseline-design.md`

## Global Constraints

- The integration base is `develop`.
- Canonical database objects use at least two-word `snake_case` names.
- Production logic and arithmetic are Rust; TypeScript is UI/client only.
- PostgreSQL is canonical; search and graph are projections.
- Keyverse is identity authority; no local passwords.
- Every tenant-owned access is database and application isolated.
- Relationship facts are first-class and bitemporal.
- External identifiers never become internal primary keys.
- Money uses exact decimal representations.
- No heuristic relationship-health or forecast scores.
- ELUNVERA-owned production statement, branch, and public API documentation coverage are each 100%.
- Every task updates relevant docs, CHANGELOG, and the gap baseline.

---

### Task 1: Establish the Rust workspace and exact quality gate

**Files:**
- Create: `Cargo.toml`
- Create: `rust-toolchain.toml`
- Create: `crates/domain_contracts/Cargo.toml`
- Create: `crates/domain_contracts/src/lib.rs`
- Create: `tests/contract/repository_layout_test.py`
- Create: `.github/workflows/product.yml`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: workspace crate `domain_contracts`; command `cargo test --workspace`; exact quality workflow.

- [ ] **Step 1: Write the failing repository contract test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_foundation_workspace_contract() -> None:
    required = [
        ROOT / "Cargo.toml",
        ROOT / "rust-toolchain.toml",
        ROOT / "crates/domain_contracts/src/lib.rs",
        ROOT / ".github/workflows/product.yml",
    ]
    assert all(path.is_file() for path in required)
```

- [ ] **Step 2: Verify the test fails**

Run: `python -m pytest tests/contract/repository_layout_test.py -q`
Expected: failure because the workspace files do not exist.

- [ ] **Step 3: Create the minimal warning-free workspace**

```rust
//! Versioned domain contracts shared by ELUNVERA foundation modules.

#![forbid(unsafe_code)]
#![deny(missing_docs)]

/// Contract version implemented by this crate.
pub const CONTRACT_VERSION: &str = "0.1.0";
```

Pin the stable compiler in `rust-toolchain.toml`, deny warnings in CI, and configure format, Clippy, test, doc, and coverage commands.

- [ ] **Step 4: Run the foundation gate**

Run:

```bash
python -m pytest tests/contract/repository_layout_test.py -q
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo doc --workspace --no-deps
```

Expected: all pass without warnings.

- [ ] **Step 5: Commit**

```bash
git add Cargo.toml rust-toolchain.toml crates tests .github CHANGELOG.md
git commit -m "build: establish Rust foundation quality gate"
```

### Task 2: Implement verified authorization context

**Files:**
- Create: `crates/authorization_context/Cargo.toml`
- Create: `crates/authorization_context/src/lib.rs`
- Create: `crates/authorization_context/tests/authorization_context.rs`
- Modify: `Cargo.toml`
- Modify: `docs/SECURITY.md`

**Interfaces:**
- Produces: `VerifiedRequestContext`, `TenantReference`, `PurposeCode`, `AuthorizationError`.

- [ ] **Step 1: Write failing context tests**

```rust
#[test]
fn caller_supplied_tenant_cannot_override_verified_tenant() {
    let context = verified_context("tenant_alpha");
    assert_ne!(context.tenant_reference().as_str(), "tenant_beta");
}

#[test]
fn missing_purpose_is_rejected() {
    let result = VerifiedRequestContext::try_new(valid_claims_without_purpose());
    assert!(matches!(result, Err(AuthorizationError::MissingPurpose)));
}
```

- [ ] **Step 2: Verify RED**

Run: `cargo test -p authorization_context`
Expected: compilation failure because the types do not exist.

- [ ] **Step 3: Implement immutable typed context**

Use private fields, validated constructors, opaque tenant/workspace references, bounded role/scope sets, UTC time checks, and no deserialization path that accepts authority directly from HTTP headers.

- [ ] **Step 4: Verify GREEN and coverage**

Run:

```bash
cargo test -p authorization_context
cargo llvm-cov -p authorization_context --branch --fail-under-lines 100 --fail-under-functions 100 --fail-under-regions 100
```

Expected: all tests pass and production coverage is complete.

- [ ] **Step 5: Commit**

```bash
git add crates/authorization_context Cargo.toml docs/SECURITY.md
git commit -m "feat: add verified tenant authorization context"
```

### Task 3: Create PostgreSQL lifecycle, RLS, and temporal schema

**Files:**
- Create: `database/migrations/0001_foundation.sql`
- Create: `database/migrations/0001_foundation.down.sql`
- Create: `tests/integration/foundation_schema.rs`
- Create: `infrastructure/compose.yaml`
- Create: `scripts/rehearse-migrations.sh`
- Modify: `docs/DATA_MODEL.md`

**Interfaces:**
- Produces: `tenant_account`, `workspace_record`, `workspace_member`, `party_record`, `commercial_account`, `relationship_record`, `relationship_participant`, `source_receipt`, `evidence_reference`, `audit_event`, `outbox_event`.

- [ ] **Step 1: Write failing migration integration tests**

Test clean migration, database object naming, RLS denial without tenant context, cross-tenant denial, temporal overlap rejection, UUIDv7 defaults, and down/up rehearsal.

- [ ] **Step 2: Start isolated PostgreSQL and verify RED**

Run:

```bash
podman compose -f infrastructure/compose.yaml -p elunvera-foundation-test up -d postgres
cargo test --test foundation_schema -- --nocapture
```

Expected: failure because migrations do not exist.

- [ ] **Step 3: Implement normalized migration**

Use tenant foreign keys, `tstzrange` valid/recorded intervals, temporal/exclusion constraints, RLS policies using transaction-local verified tenant settings, exact audit and outbox fields, and no business-critical JSONB.

- [ ] **Step 4: Rehearse and verify GREEN**

Run:

```bash
./scripts/rehearse-migrations.sh
cargo test --test foundation_schema -- --nocapture
```

Expected: clean install, down/up rehearsal, tenant attacks, and temporal constraints pass.

- [ ] **Step 5: Remove isolated runtime and commit**

```bash
podman compose -f infrastructure/compose.yaml -p elunvera-foundation-test down -v
git add database tests/integration infrastructure scripts docs/DATA_MODEL.md
git commit -m "feat: add tenant-isolated temporal CRM schema"
```

### Task 4: Implement account, party, and relationship domain modules

**Files:**
- Create: `crates/account_registry/src/lib.rs`
- Create: `crates/party_registry/src/lib.rs`
- Create: `crates/relationship_registry/src/lib.rs`
- Create: `crates/*/tests/*.rs`
- Modify: `Cargo.toml`

**Interfaces:**
- Produces: `CreateAccountCommand`, `CreatePartyCommand`, `RecordRelationshipCommand`, `AccountRepository`, `PartyRepository`, `RelationshipRepository`, domain events from `domain_contracts`.
- Consumes: `VerifiedRequestContext` and schema from Tasks 2–3.

- [ ] **Step 1: Write failing state and property tests**

Cover account creation, local party identity, n-ary relationship participants, evidence-or-manual-assertion requirement, time intervals, exclusive-role overlap, truth status, cross-tenant rejection, and correction without history deletion.

- [ ] **Step 2: Verify RED**

Run: `cargo test -p account_registry -p party_registry -p relationship_registry`.

- [ ] **Step 3: Implement minimal domain behavior**

Keep aggregate invariants in pure Rust types, persistence behind traits, errors exhaustive, and public APIs fully documented. Do not introduce a graph database dependency.

- [ ] **Step 4: Verify property and mutation boundaries**

Run:

```bash
cargo test -p account_registry -p party_registry -p relationship_registry
cargo llvm-cov --workspace --branch --fail-under-lines 100
```

Expected: all state transitions, negative branches, and production lines pass.

- [ ] **Step 5: Commit**

```bash
git add crates Cargo.toml
git commit -m "feat: implement account and relationship kernel"
```

### Task 5: Implement idempotent HTTP commands and operation receipts

**Files:**
- Create: `apps/elunvera_api/Cargo.toml`
- Create: `apps/elunvera_api/src/main.rs`
- Create: `apps/elunvera_api/src/routes/accounts.rs`
- Create: `apps/elunvera_api/src/routes/relationships.rs`
- Create: `apps/elunvera_api/tests/http_contract.rs`
- Modify: `schemas/openapi.yaml`

**Interfaces:**
- Produces: `/v1/accounts`, `/v1/parties`, `/v1/relationships`; RFC 9457 errors; ETag; operation receipt.
- Consumes: domain commands and verified context.

- [ ] **Step 1: Write failing HTTP contract tests**

Test missing/invalid identity, missing idempotency key, same-key same-payload replay, same-key different-payload conflict, stale `If-Match`, cross-tenant not-found, payload limit, and safe error copy.

- [ ] **Step 2: Verify RED**

Run: `cargo test -p elunvera_api --test http_contract`.

- [ ] **Step 3: Implement minimal Axum routes**

Validate OpenAPI schemas, construct authority only from middleware, commit aggregate and outbox in one transaction, return receipt and ETag, and map errors to stable Problem Details.

- [ ] **Step 4: Validate contract and tests**

```bash
cargo test -p elunvera_api
python scripts/validate-contracts.py
```

Expected: HTTP behavior and OpenAPI operation IDs are consistent.

- [ ] **Step 5: Commit**

```bash
git add apps schemas scripts
git commit -m "feat: expose idempotent CRM foundation API"
```

### Task 6: Implement outbox worker and account read projection

**Files:**
- Create: `apps/elunvera_worker/Cargo.toml`
- Create: `apps/elunvera_worker/src/main.rs`
- Create: `crates/integration_outbox/src/lib.rs`
- Create: `crates/account_projection/src/lib.rs`
- Create: `tests/integration/outbox_projection.rs`
- Modify: `schemas/asyncapi.yaml`

**Interfaces:**
- Produces: account/relationship CloudEvents and `AccountOverviewProjection`.
- Consumes: transactional outbox records.

- [ ] **Step 1: Write failing duplicate, reorder, and crash tests**

Prove one projection effect after duplicate delivery, recovery after worker termination between claim and completion, dead-letter isolation, and no authority flowing from projection to canonical tables.

- [ ] **Step 2: Verify RED**

Run: `cargo test --test outbox_projection -- --nocapture`.

- [ ] **Step 3: Implement leasing, publishing, inbox receipt, and projection**

Use bounded batches, heartbeat, retry classification, low-cardinality metrics, schema validation, and atomic projection receipt.

- [ ] **Step 4: Verify GREEN**

Run the test with repeated randomized delivery sequences and confirm the same final projection hash.

- [ ] **Step 5: Commit**

```bash
git add apps/elunvera_worker crates/integration_outbox crates/account_projection tests schemas/asyncapi.yaml
git commit -m "feat: project account context from durable events"
```

### Task 7: Build the accessible three-band account interface

**Files:**
- Create: `apps/elunvera_web/`
- Create: `packages/design_tokens/`
- Create: `apps/elunvera_web/stories/`
- Create: `apps/elunvera_web/e2e/account-overview.spec.ts`
- Modify: `docs/UX_SPEC.md`
- Modify: `docs/adr/0014-ux-design-system.md`

**Interfaces:**
- Produces: `AccountOverviewPage`, three band components, relationship table/graph toggle, evidence drawer, responsive and print views.
- Consumes: generated TypeScript client and `AccountOverviewProjection`.

- [ ] **Step 1: Create and record the Figma library**

Create reviewed desktop, tablet, mobile, Korean, English, print, loading, empty, stale, conflict, denied, and provider-unavailable frames. Record the real Figma File ID in ADR-0014; do not use a placeholder.

- [ ] **Step 2: Write failing Storybook and Playwright interactions**

Test keyboard band navigation, evidence drawer focus, graph-to-table parity, Korean/English rendering, stale state, safe next-action copy, and print exact values.

- [ ] **Step 3: Verify RED**

Run:

```bash
pnpm --dir apps/elunvera_web test
pnpm --dir apps/elunvera_web test-storybook
pnpm --dir apps/elunvera_web playwright test
```

Expected: failures because components do not exist.

- [ ] **Step 4: Implement from shared tokens**

Use accessible semantic HTML, progressive enhancement, bounded graph rendering, no internal service names, and no color-only states.

- [ ] **Step 5: Validate screenshots and accessibility, then commit**

```bash
pnpm --dir apps/elunvera_web lint
pnpm --dir apps/elunvera_web typecheck
pnpm --dir apps/elunvera_web test --coverage
pnpm --dir apps/elunvera_web test-storybook
pnpm --dir apps/elunvera_web playwright test

git add apps/elunvera_web packages/design_tokens docs
git commit -m "feat: add accessible three-band account workspace"
```

### Task 8: Complete operability, security, restoration, and release evidence

**Files:**
- Create: `crates/telemetry/`
- Create: `apps/elunvera_api/src/health.rs`
- Create: `infrastructure/otel/`
- Create: `scripts/rehearse-restore.sh`
- Create: `docs/runbooks/foundation-incident.md`
- Create: `docs/validation/foundation-release-evidence.md`
- Modify: `docs/OPERABILITY.md`
- Modify: `docs/product-technical-gap-baseline.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: `/healthz`, `/startupz`, `/readyz`, OTLP signals, restore receipt, release evidence manifest.

- [ ] **Step 1: Write failing health, telemetry privacy, and restore tests**

Prove liveness does not depend on DB, readiness fails without safe write/key/queue path, traces contain no fixture PII, and a restored environment preserves tenant/RLS/outbox/projection integrity.

- [ ] **Step 2: Verify RED**

Run the focused tests and restoration script; expect missing implementation failures.

- [ ] **Step 3: Implement minimal operational path**

Add low-cardinality metrics, correlation propagation, bounded status output, graceful drain, encrypted backup integration, and isolated restoration verification.

- [ ] **Step 4: Run complete current-head evidence suite**

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo nextest run --workspace --all-features
cargo llvm-cov --workspace --branch --fail-under-lines 100
python scripts/validate-contracts.py
./scripts/rehearse-migrations.sh
./scripts/rehearse-restore.sh
pnpm --dir apps/elunvera_web verify
```

Expected: every required check passes on the same exact head with no skipped release lane.

- [ ] **Step 5: Update evidence and commit**

```bash
git add crates/telemetry apps infrastructure scripts docs CHANGELOG.md
git commit -m "ops: complete ELUNVERA foundation readiness evidence"
```

## Plan completion gate

The foundation is complete only when a target user can authenticate, create an account and parties, record and correct an evidence-linked time-valid relationship, view the accessible three-band account page, inspect the audit and operation receipt, and recover the same result from a tested backup without crossing tenant boundaries.
