# ELUNVERA Storybook Inventory

## Foundations

- typography and locale samples;
- spacing, radius, elevation, and motion tokens;
- semantic state tokens: authoritative, observed, inferred, proposed, disputed, rejected, superseded;
- focus, disabled, read-only, error, warning, and success states;
- account and data-classification badges;
- exact-value and print tokens.

## Navigation and layout

- `GlobalNavigation`;
- `WorkspaceSwitcher`;
- `TemporalLensBar`;
- `ThreeBandAccountLayout`;
- `EvidenceDrawer`;
- `ContextualActionBar`;
- `ResponsiveSideSheet`.

## Domain components

- `AccountHeader`;
- `AccountContextBand`;
- `RelationshipStructureBand`;
- `ActionRiskBand`;
- `StakeholderTree`;
- `RelationshipGraph`;
- `RelationshipTable`;
- `TruthStatusBadge`;
- `EvidenceReferenceList`;
- `TemporalFactCard`;
- `CommitmentCard`;
- `CommitmentQueue`;
- `OpportunityStageHistory`;
- `ForecastSnapshotCard`;
- `ComplaintTimeline`;
- `OutcomeTracker`;
- `ModelClaimCard`;
- `ReviewDecisionPanel`;
- `OperationReceiptPanel`;
- `DataRightsExportPreview`.

## Form patterns

- time-valid relationship editor;
- opportunity stage-transition form;
- exact-money input with currency;
- evidence attachment selector;
- manual-assertion disclosure;
- conflict resolution form;
- account merge comparison;
- purpose and disclosure policy selector;
- destructive action preview.

## Required scenes for every component

```text
default
hover where meaningful
keyboard focus
touch interaction
loading
empty
partial
stale
conflict
access denied
offline
error
success
high zoom
reduced motion
Korean
English
print
```

## Event definitions

Storybook interaction tests must emit semantic product events rather than DOM implementation details. Examples:

```text
account_brief_opened
relationship_evidence_opened
truth_status_review_started
opportunity_stage_change_proposed
commitment_status_changed
complaint_remedy_reviewed
model_claim_reviewed
export_preview_opened
```

Events exclude raw names, notes, message bodies, contact details, and unrestricted tenant identifiers.

## Accessibility evidence

Each interactive story includes automated accessibility checks, keyboard script, expected accessible name and role, focus sequence, reduced-motion behavior, and screen-reader notes for dynamic updates. Graph stories include a synchronized structured table.
