# ELUNVERA Low-Fidelity Wireframes

These diagrams define information priority, not final visual styling.

## Account overview — desktop

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Global navigation     Search                 Purpose / Profile       │
├─────────────────────────────────────────────────────────────────────┤
│ ACME Manufacturing      Active account      Last verified: today    │
│ Owner · Segment · Region · Hierarchy             [Prepare meeting]  │
├──────────────────── ACCOUNT CONTEXT ────────────────────────────────┤
│ Desired outcomes │ Commercial scope │ Recent change │ Data freshness│
├────────────────── RELATIONSHIP STRUCTURE ──────────────────────────┤
│ Organization / stakeholder tree     │ Internal account team         │
│ Relationship graph/table toggle     │ Evidence and temporal lens    │
├──────────────────── ACTION AND RISK ────────────────────────────────┤
│ Commitments │ Opportunity decisions │ Complaints │ Proposed reviews │
└─────────────────────────────────────────────────────────────────────┘
```

## Relationship evidence drawer

```text
┌─────────────────────────────────────┐
│ Procurement lead                    │
│ Truth: observed · Current           │
│ Valid from: 2026-08-25              │
│ Recorded: 2026-08-27                │
├─────────────────────────────────────┤
│ Evidence 1 · public announcement    │
│ Evidence 2 · verified meeting       │
│ Older conflict · email signature    │
├─────────────────────────────────────┤
│ [Correct] [Reject] [Add evidence]   │
└─────────────────────────────────────┘
```

## Opportunity review

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Opportunity · Current stage · Process version · Currency / value    │
├───────────────────────────┬─────────────────────────────────────────┤
│ Stage history             │ Decision evidence                       │
│ Discover                  │ Stakeholders and roles                  │
│ Validate                  │ Assumptions and unresolved questions    │
│ Propose                   │ Forecast snapshot with uncertainty      │
├───────────────────────────┴─────────────────────────────────────────┤
│ [Propose stage change] [Record forecast] [Link customer outcome]    │
└─────────────────────────────────────────────────────────────────────┘
```

## Mobile account flow

```text
[Account header]
[Context band]
[Relationship summary]
[Open relationship explorer]
[Action queue]
[Primary action sheet]
```

## Required edge-state frames

```text
loading
no account data
partial connector data
stale evidence
conflicting claims
access denied
provider unavailable
offline draft
optimistic conflict
long job running
job failed with recovery
legal hold prevents deletion
```
