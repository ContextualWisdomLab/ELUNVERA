# ADR 0017: ELUNVERA is the relationship-activation home

- **Status:** Proposed
- **Date:** 2026-08-27
- **Reconciled:** 2026-09-02
- **Scope:** ContextualWisdomLab/ELUNVERA

## Problem

ContextualWisdomLab already has products that own lineage, retrieval, semantic publication/catalog, employment truth, and identity. None owns the operational decision “what should I do next to keep this known relationship moving, and what receipt proves what happened?”

## Constraints

ELUNVERA must remain independently deployable, consume neighboring products only through released contracts/ACLs, avoid cross-service SQL and copied source, preserve tenant boundaries, and never use synthetic demonstration records as production inputs.

## Alternatives

1. Put relationship activation into LineageWeave. Rejected: lineage provenance and operational next-move state have different aggregates and release cadence.
2. Put it into a CRM/customer-master monolith. Rejected: it duplicates employment, identity, retrieval, and catalog authorities and creates an oversized shared kernel.
3. Keep a bounded relationship-activation context in ELUNVERA. **Selected.** It gives the customer one action-oriented home while preserving explicit upstream authorities.

## Decision

The first customer-visible surface is the **Activation Queue**. A `RelationshipActivation` aggregate owns one known relationship reference, its current next move, and its transition invariant. Activate, Reschedule, and Dismiss are domain commands. Durable production work will persist immutable `ActivationReceipt` events and rebuild current queue state from ELUNVERA-owned records, not from another product’s database.

The executable first slice remains a prototype and therefore this ADR remains **Proposed**. Runtime startup is empty. Anonymized synthetic fixtures exist only under tests.

## Context map

- **ELUNVERA Relationship Activation (core):** relationship activation aggregate, queue projection, action receipt.
- **ELUNVERA Interaction/Delivery (supporting):** HTTP/browser presentation and API command boundary.
- **keyverse Identity (upstream):** released identity/token contract consumed through an ACL.
- **LineageWeave Provenance (upstream):** optional released evidence identifiers consumed through an ACL; no lineage writes.
- **RankWeave Retrieval (upstream, future):** candidate retrieval only if a released contract is needed; no fusion logic locally.
- **ConceptWeave / semantic-data-portal (upstream, future):** released semantic/catalog contracts; ELUNVERA retains relationship domain truth.
- **Orgmetra (upstream):** employment/organization truth only; ELUNVERA stores references needed for activation, not employment records.

## Ubiquitous language and invariants

- **RelationshipActivation:** aggregate root for one tenant-scoped known relationship’s operational next move.
- **ActivationMove:** value describing the next action, due date, and why-now evidence.
- **ActivationReceipt:** immutable evidence that an allowed transition occurred.
- **RelationshipReference:** value identifying parties without taking ownership of upstream domain truth.
- **ActivationQueue:** read projection of due/rescheduled aggregates.

Invariants: only allowed commands transition state; reschedule requires a valid due date; activated/dismissed work leaves the home projection; one command transaction mutates at most one aggregate; duplicate command delivery must be idempotent once persistence lands; cross-product references remain references, not local copies of source-of-truth records.

## Consequences and risks

The current Python/in-memory adapter is not production persistence and must not be described as shippable. The next causal slice is a real-data repository port plus 3NF PostgreSQL adapter, identity/tenant authorization, and immutable receipt/idempotency tests. Until an upstream owner has an immutable release, integrations use a port/ACL/feature flag/test double rather than source/DB/temp-branch coupling.

## Follow-up evidence

Before this ADR can become Accepted: exact-head CI/security/review evidence, durable restart-safe workflow, migration/backup/restore evidence, realistic web performance, accessibility/i18n evidence, and an immutable release contract must be demonstrated.
