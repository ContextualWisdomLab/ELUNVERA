# ELUNVERA Architecture Decision Records

Status values: `Proposed`, `Accepted`, `Superseded`, `Rejected`.

| ADR | Decision | Status |
|---|---|---|
| [0001](./0001-product-boundary.md) | Own CRM truth; federate adjacent products | Proposed |
| [0002](./0002-modular-monolith.md) | Begin as a modular monolith | Proposed |
| [0003](./0003-keyverse-identity.md) | Use Keyverse as identity authority | Proposed |
| [0004](./0004-bitemporal-truth.md) | Represent relationship truth bitemporally | Proposed |
| [0005](./0005-first-class-relationships.md) | Make relationships first-class records | Proposed |
| [0006](./0006-provider-neutral-integrations.md) | Use capability-specific integration ports | Proposed |
| [0007](./0007-purpose-aware-privacy.md) | Use purpose-aware field selection instead of universal masking | Proposed |
| [0008](./0008-ai-human-judgment.md) | Separate model claims from authoritative facts | Proposed |
| [0009](./0009-postgresql-system-of-record.md) | Use PostgreSQL 18 as canonical system of record | Proposed |
| [0010](./0010-rust-compute-boundary.md) | Use Rust for production computation and prohibit heuristic scores | Proposed |
| [0011](./0011-contract-versioning.md) | Version HTTP and events independently | Proposed |
| [0012](./0012-quality-release-gates.md) | Require evidence-based release gates | Proposed |
| [0013](./0013-brand-and-license.md) | Preserve brand boundaries; license original source under Apache-2.0 | Accepted |
| [0014](./0014-ux-design-system.md) | Use a three-band account UX and shared design system | Proposed |
| [0015](./0015-retention-disposition.md) | Make retention, legal hold, and disposition explicit workflows | Proposed |
| [0016](./0016-cwl-ecosystem-boundaries.md) | Integrate CWL products without direct SQL or code copying | Proposed |
