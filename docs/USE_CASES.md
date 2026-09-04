# ELUNVERA Use Cases

## UC-01 Prepare for a customer meeting

**Actor:** Account owner
**Preconditions:** Verified tenant access and account-management purpose.
**Flow:** Open account → apply current temporal lens → review context, relationships, commitments, opportunities, complaints, and recent changes → open evidence for consequential claims → generate a bounded meeting brief → approve export.
**Postcondition:** Brief manifest and access receipt exist; no source system is mutated.

## UC-02 Record and revise a stakeholder relationship

**Actor:** Account-team member
**Flow:** Select parties → choose versioned relationship type → enter valid interval and account context → link evidence or mark manual assertion → save with idempotency key → later close or correct interval through a new version.
**Exceptions:** Cross-tenant party, overlapping exclusive role, stale ETag, insufficient purpose.
**Postcondition:** Historical relationship remains queryable.

## UC-03 Progress an opportunity

**Actor:** Account executive
**Flow:** Review current process version → propose stage transition → enter effective time, reason, evidence, and changed assumptions → server validates allowed transition → commit opportunity and outbox event atomically.
**Postcondition:** Prior stage and forecast snapshots are immutable.

## UC-04 Resolve conflicting roles

**Actor:** Account owner or data steward
**Flow:** System displays two current role claims → compare sources and temporal intervals → accept, correct, reject, or preserve both as context-specific → record review decision.
**Postcondition:** Truth status changes are explicit; source evidence remains.

## UC-05 Import external CRM data

**Actor:** Tenant administrator
**Flow:** Register provider and mapping → upload or connect bounded source → dry-run validation and duplicate report → approve batch → item-level idempotent ingestion → reconcile counts and errors.
**Postcondition:** Provider IDs live only in mapping records; malformed items are reported rather than silently dropped.

## UC-06 Merge duplicate accounts

**Actor:** Data steward with maker-checker approval
**Flow:** Request dry-run → compare fields, relationships, interactions, opportunities, privacy policies, and external mappings → choose canonical survivor without deleting source identities → independent approval → execute → verify projections.
**Postcondition:** Merge receipt supports reversal or split.

## UC-07 Protect a commitment

**Actor:** Account manager
**Flow:** Record commitment with owner, beneficiary, status, due interval, and evidence → observe updates from calendar/email by reference → review conflict → confirm action or delegate execution to ScopeWeave.
**Postcondition:** ELUNVERA owns commitment truth, not external task execution.

## UC-08 Manage a complaint

**Actor:** Complaint owner
**Flow:** Record complaint and channel → classify impact without arbitrary severity score → investigate evidence → propose remedy → record customer response → verify follow-up and outcome.
**Postcondition:** Complaint lifecycle is linked to account, interactions, outcomes, and corrective action.

## UC-09 Review a model claim

**Actor:** Authorized human reviewer
**Flow:** Open proposed claim → inspect model, prompt, evidence, uncertainty, subgroup limitations, and validation status → accept as reviewed inference, reject, or request more evidence.
**Postcondition:** Review cannot convert the claim into a different underlying fact without a separate domain command.

## UC-10 Fulfill a data-access request

**Actor:** Privacy operations user
**Flow:** Verify requester → scope identities and tenants → collect authorized fields and sources → review exclusions → generate encrypted export → deliver with expiration → record receipt.
**Postcondition:** The case preserves the basis for inclusion and exclusion.

## UC-11 Restore after an incident

**Actor:** Operations engineer
**Flow:** Create isolated environment → restore database and object artifacts → load correct keys and release manifest → replay migrations and outbox safely → rebuild projections → run integrity and tenant tests → approve service return.
**Postcondition:** Restoration evidence is retained and gaps become remediation items.
