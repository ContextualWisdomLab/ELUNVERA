# ELUNVERA Security Architecture

- **Document version:** 0.1
- **Status:** Proposed security baseline
- **Date:** 2026-08-27

## 1. Security objective

Protect customer relationship data, commercial strategy, communications metadata, opportunity value, complaints, identity links, and model evidence while preserving authorized operational use. ELUNVERA uses strong identity, tenant isolation, purpose-aware authorization, field selection, encryption, immutable audit, and bounded integration rather than universal destructive masking.

## 2. Control framework baseline

The product design is aligned to, but does not claim certification against:

- ISO/IEC 27001:2022 and Amendment 1:2024;
- ISO/IEC 27701:2025;
- NIST Cybersecurity Framework 2.0;
- NIST Privacy Framework 1.0, while tracking the draft 1.1 revision;
- OWASP ASVS and OWASP API Security Top 10;
- SOC 2 trust-services concerns for security, availability, confidentiality, processing integrity, and privacy;
- Korean Personal Information Protection Act and its current Enforcement Decree;
- GDPR where territorial scope applies.

Certification, legal compliance, or audit readiness requires implementation and independent evidence beyond these documents.

## 3. Security boundaries

### Trusted control plane

- verified Keyverse identity context;
- authorization policy and purpose registry;
- canonical PostgreSQL system of record;
- cryptographic key-management interface;
- append-only audit and operation receipts.

### Untrusted inputs

- connector payloads;
- email and calendar observations;
- uploaded files and note content;
- webhooks;
- LLM output;
- imported CRM data;
- user-entered rich text;
- cross-tenant identifiers supplied by callers.

Untrusted content remains data. It cannot alter authorization, tool permissions, model instructions, retention policy, or tenant scope.

## 4. Identity and access control

- Keyverse is the identity authority; ELUNVERA stores subject mappings, not passwords.
- OIDC validation checks exact issuer, audience, signature, token type, nonce where applicable, `nbf`, `iat`, and `exp`.
- Human, service, workflow, and delegated-agent principals are distinct.
- SCIM drives joiner, mover, and leaver lifecycle where configured.
- Role-based access is necessary but insufficient; every sensitive operation also evaluates tenant, workspace, relationship context, purpose, data classification, disclosure policy, and legal hold.
- Privileged changes such as bulk export, account merge, high-volume deletion, model release, and policy override require maker-checker approval.
- Guessed cross-tenant identifiers return a non-disclosing `404`.

## 5. Tenant isolation

Defense in depth includes:

1. verified tenant context at ingress;
2. domain repository methods requiring that context;
3. PostgreSQL row-level security or an equivalent database-enforced boundary;
4. tenant-bound object-storage prefixes and encryption context;
5. tenant-bound search and graph projection namespaces;
6. contract tests proving cross-tenant access returns no data;
7. telemetry that omits raw tenant PII.

A background worker may not bypass tenant enforcement merely because it is internal. It uses a scoped service principal and explicit job tenant.

## 6. Data protection

### In transit

- TLS 1.3 preferred; TLS 1.2 permitted only where a reviewed compatibility profile requires it.
- Remote PostgreSQL connections use certificate verification.
- Service identities use short-lived credentials.

### At rest

- Storage encryption uses customer- or environment-scoped keys.
- Highly restricted fields may use application-level envelope encryption with versioned key references.
- Key rotation supports active and predecessor keys, bounded re-encryption jobs, receipts, and rollback.
- Backups are encrypted and restoration verifies key availability.

### Field exposure

API schemas define field classifications and purpose-specific views. The server excludes fields not needed for the approved purpose. Logging and analytics do not receive full record objects.

## 7. Secrets

- Secrets reside in a managed secret store or KMS-integrated vault.
- Source code, CI logs, events, traces, screenshots, fixtures, and support bundles contain no live secrets.
- Provider credentials are not distributed to every domain service; capability adapters receive only the credential they require.
- Secret rotation is tested without service redeployment where the provider permits it.

## 8. Integration security

Every adapter enforces:

- exact destination host and port policy;
- allowed methods and content types;
- DNS-rebinding resistance;
- connection, request, and response timeouts;
- request and response size limits;
- redirect policy;
- signature or mutual-authentication verification;
- idempotency and replay defense;
- bounded retry with jitter;
- circuit breaking without data loss;
- source receipt and payload hash.

A webhook is an external assertion. Signature verification, replay checks, and state-transition validation precede any canonical mutation.

## 9. Content security

- Rich text is stored in a safe structured representation and rendered through an allowlist sanitizer.
- JavaScript, macros, executable attachments, and external resource fetching are disabled in parsing workflows.
- File type is established from signatures and bounded parsing, not filename extension or caller `Content-Type` alone.
- Malware scanning and quarantine precede attachment availability.
- Spreadsheet exports neutralize formula injection.
- CSV, JSON, PDF, and Office exports preserve classification and access receipts.

## 10. AI security

- LLM calls go through contextual-orchestrator.
- Customer text is untrusted observation, never system instruction.
- Prompt templates, tool capability lists, model identity, provider, reasoning level, and evidence set are versioned.
- Models never receive credentials or unrestricted cross-tenant context.
- Tools are typed, bounded, and purpose-scoped.
- High-impact mutations terminate at human approval.
- Model claims are stored separately from authoritative facts.
- Indirect prompt-injection, data exfiltration, unsupported claim, and tool-escalation tests are release gates.

## 11. Audit integrity

Audit events include actor, tenant, purpose, command, target reference, prior and resulting versions, recorded time, correlation, decision reference, and policy outcome. High-volume raw content is referenced by digest rather than copied into the audit log.

Audit rows are append-only. Corrections append compensating records. Retention and legal-hold policy governs deletion; administrators cannot silently erase privileged actions.

## 12. Availability and abuse resistance

- Per-principal and per-tenant rate and concurrency limits.
- Bounded page size, query depth, export size, graph traversal, and batch item count.
- Queue admission control and backpressure.
- Memory, CPU, database connection, and external-call budgets.
- Async jobs for expensive work.
- Tenant isolation of noisy workloads.
- Administrative emergency read-only mode.

## 13. Supply chain

- Dependencies and actions pinned by digest or full commit SHA.
- Rust lockfile and frontend lockfile are reviewed and immutable in release builds.
- SBOM uses SPDX.
- Builds generate provenance and signed artifacts.
- License, vulnerability, secret, SAST, dependency-review, and artifact-integrity checks are required.
- Release jobs use short-lived identity rather than long-lived publishing keys where supported.

## 14. Security acceptance criteria

A GA candidate must demonstrate:

- zero unauthorized cross-tenant reads or writes in the adversarial suite;
- zero unauthenticated remote business endpoints;
- successful key rotation and restore rehearsals;
- duplicate and reordered webhook safety;
- bounded hostile payload handling;
- prompt-injection action-escalation rate of zero in the release corpus;
- no raw secrets or restricted PII in telemetry and build artifacts;
- independent security review of current-head code;
- documented residual risks and approved owners.
