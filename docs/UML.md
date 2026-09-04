# ELUNVERA UML and Behavioral Models

## 1. Component model

```mermaid
flowchart TB
    Web[ELUNVERA Web] --> API[ELUNVERA API]
    Admin[Admin Console] --> API
    API --> Auth[Authorization Context]
    API --> Accounts[Account and Party Modules]
    API --> Relations[Relationship Module]
    API --> Commercial[Opportunity and Commitment Modules]
    API --> Outcomes[Outcome and Complaint Modules]
    API --> Privacy[Privacy and Rights Module]
    Accounts --> DB[(PostgreSQL)]
    Relations --> DB
    Commercial --> DB
    Outcomes --> DB
    Privacy --> DB
    API --> Outbox[Transactional Outbox]
    Outbox --> Worker[Worker]
    Worker --> Projection[Search and Graph Read Models]
    Worker --> Adapters[CWL Capability Adapters]
```

## 2. Account aggregate sequence

```mermaid
sequenceDiagram
    actor User
    participant Web
    participant API
    participant Policy
    participant DB
    participant Outbox

    User->>Web: Save account change
    Web->>API: PATCH + If-Match + Idempotency-Key
    API->>Policy: authorize(context, purpose, fields)
    Policy-->>API: permit + field policy
    API->>DB: begin transaction
    API->>DB: verify version and apply temporal fact
    API->>Outbox: append account.changed event
    API->>DB: commit
    API-->>Web: operation receipt + new ETag
```

## 3. Model-claim review sequence

```mermaid
sequenceDiagram
    participant Worker
    participant Orchestrator as contextual-orchestrator
    participant DB
    actor Reviewer

    Worker->>Orchestrator: evidence bundle + strict schema
    Orchestrator-->>Worker: proposed claim + uncertainty + trace
    Worker->>DB: store model_claim(proposed)
    Reviewer->>DB: read claim and evidence
    Reviewer->>DB: record review decision
    Note over Reviewer,DB: A separate domain command is required to change authoritative facts
```

## 4. Opportunity state model

```mermaid
stateDiagram-v2
    [*] --> Open
    Open --> Qualified: allowed process transition
    Qualified --> Validated
    Validated --> Proposed
    Proposed --> Negotiating
    Negotiating --> Won
    Negotiating --> Lost
    Open --> Disqualified
    Qualified --> Disqualified
    Validated --> Disqualified
    Won --> [*]
    Lost --> [*]
    Disqualified --> [*]
```

The actual stages and allowed transitions are versioned per tenant. This diagram is an illustrative default, not a hard-coded sales methodology.

## 5. Complaint state model

```mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Acknowledged
    Acknowledged --> Investigating
    Investigating --> RemedyProposed
    RemedyProposed --> RemedyDelivered
    RemedyDelivered --> FollowUp
    FollowUp --> Closed
    Received --> Withdrawn
    Investigating --> Withdrawn
```

## 6. Truth-status state model

```mermaid
stateDiagram-v2
    Proposed --> ReviewedInference: accepted as inference
    Proposed --> Rejected
    Observed --> Superseded
    Authoritative --> Superseded
    ReviewedInference --> Superseded
    Observed --> Disputed
    Authoritative --> Disputed
    Disputed --> Superseded
```

No state transition automatically converts an inference into an authoritative source fact.
