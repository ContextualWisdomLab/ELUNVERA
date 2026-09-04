# ELUNVERA PRD — relationship activation

**Product:** ELUNVERA  
**Tagline:** Every Link, Understood. Every Relationship, Activated.  
**Updated:** 2026-09-02  
**Status:** Proposed prototype evidence; not yet shippable

## Problem and customer job

A known relationship goes quiet because no product owns the next concrete move. The customer already knows the parties and needs one place to understand what should happen next, why it matters now, and whether the move was activated, rescheduled, or dismissed.

## Core outcome

ELUNVERA turns a known relationship into an actionable, evidence-linked next move and preserves the resulting action receipt without becoming the system of record for lineage, retrieval, ontology, employment, or identity.

## Current prototype scope

1. Open a local activation-queue home.
2. Render known relationships as parties, kind, next move, due date, and why-now evidence.
3. Apply **Activate**, **Reschedule**, or **Dismiss** transitions.
4. Sort due/rescheduled work by due date.
5. Start with an empty runtime. Synthetic records exist only as anonymized unit/integration-test fixtures.

## Commercialization acceptance

The product is not shippable until a real customer can complete the workflow against durable, tenant-scoped records. Minimum evidence includes:

- released keyverse-backed identity integration through an ACL;
- 3NF PostgreSQL persistence for relationship records, activation moves, and immutable action receipts with explicit item-level UPSERT/idempotency contracts;
- provenance/reference contracts for optional LineageWeave evidence without cross-service SQL;
- asynchronous web handling and realistic k6 evidence showing each buyer-facing page p95 <= 20 ms under a documented load profile;
- keyboard, responsive, screen-reader, locale, empty/loading/error/permission interaction evidence;
- backup/restore, migration, audit, security and operability evidence appropriate for CSAP/SOC 2 design goals;
- no production consumption of synthetic demonstration data.

## Out of scope

ELUNVERA does not own lineage graph editing, retrieval/ranking, ontology publication, employment truth, identity authority, mail chrome, or a generalized customer-master database. Neighbor integrations consume immutable released contracts behind ACLs.

## Success metric for the next bounded slice

A tenant-scoped authenticated user can create or import one real relationship record, see a valid next move, apply one transition idempotently, and retrieve the immutable receipt after process restart, with exact-head tests and operational evidence.
