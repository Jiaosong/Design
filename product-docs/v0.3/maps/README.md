# OLEANDER Visual Product Maps v0.3

[← v0.3 Package](../README.md) · [Node Graph](../nodes/README.md)

> Maps are **views of nodes and relations**, not new product authorities.

---

# Map 01｜Product Mindmap

```mermaid
mindmap
  root((OLEANDER))
    Customer_Value
      Continue_correctly
      Explore_meaningfully
      Make_real_artifact
      Human_controls_key_decisions
      Recover_locally
    Product_Surfaces
      HOME
      FOCUS
      STUDIO
        EXPLORE
        DEVELOP
        SYNTHESIZE
      COMPARE
      MAP
      ARTIFACTS
      REVIEW
      KNOWLEDGE
      HISTORY
    Cross_Product
      SESSION_KERNEL
      PEOPLE_AUTHORITY
      INTEGRATIONS
      SETTINGS
      SYSTEM_HEALTH
```

---

# Map 02｜Core Human–AI Loop

```mermaid
flowchart LR
    U[Human intent] --> RES[Resume / Resolve]
    RES --> Q[Current Design Question]
    Q --> EX[Explore]
    EX --> MK[Make real artifact]
    MK --> RB[Readback]
    RB --> CR[Critique]
    CR --> CH{Human decision needed?}
    CH -- No --> DV[Develop / Repair]
    CH -- Yes --> ST[Human Steer]
    ST --> DV
    DV --> MK
    RB --> UP[Update owner-native project state via existing owner]
    UP --> NX[Continue]
```

---

# Map 03｜Autonomy × Control

```mermaid
flowchart TD
    A[Next action] --> R{Reversible?}
    R -- No --> H[Human authorization / authority route]
    R -- Yes --> S{Scope + Current fresh?}
    S -- No --> G[Mutation Guard / Re-resolve]
    S -- Yes --> V{Human-only value decision?}
    V -- Yes --> H
    V -- No --> X[Auto-advance allowed]
    X --> B[Actual result]
    B --> C[Readback]
```

---

# Map 04｜Artifact Truth Chain

```mermaid
flowchart LR
    Q[Design Question] --> REL[Design Relation]
    REL --> ART[Artifact]
    ART --> REV[Revision]
    REV --> RB[Readback]
    RB --> FIND[Finding]
    FIND --> ACT[Design Action]
    ACT --> REV2[New Revision]
    REV2 --> RB2[Re-readback]
    EVID[Evidence] --> Q
    EVID --> FIND
```

---

# Map 05｜Verification vs Validation

```mermaid
flowchart TD
    CLAIM[Design / Product Claim] --> X{What are we asking?}
    X -->|Implemented as specified?| VFY[Verification]
    X -->|Works for real user/context?| VAL[Validation]
    VFY --> E1[Requirement-matched evidence]
    VAL --> E2[Scenario / behaviour / outcome]
    E1 --> D[Design decision]
    E2 --> D
    D -->|Contradiction| R[Reframe / Revise]
```

---

# Map 06｜Decision Chain

```mermaid
flowchart LR
    P[Problem] --> Q[Question]
    Q --> O[Options]
    O --> C[Compare]
    C --> T[Trade-offs]
    T --> H[Human decision]
    H --> R[Rationale]
    R --> RC[Reopen condition]
    H --> A[Artifact change]
    A --> RB[Readback]
```

---

# Map 07｜Product Operating Loop

```mermaid
flowchart LR
    C[Customer problem] --> S[Strategy / PRFAQ]
    S --> P[Master PRD]
    P --> N[Node Specs]
    N --> B[Build]
    B --> E[Eval / Pilot]
    E --> M[Metrics]
    M --> L[Launch Readiness]
    L --> D{Decision}
    D -->|Continue| R[Roadmap]
    D -->|Iterate| P
    D -->|Reframe| S
    D -->|Stop| X[Close / Preserve Learning]
```

---

# Map 08｜Release Gates

```mermaid
flowchart TD
    A[Internal Reference] --> B{Core semantics pass?}
    B -- No --> A
    B -- Yes --> C[Closed External Pilot]
    C --> D{Value + guardrails?}
    D -- No --> E[Iterate / Reframe]
    D -- Yes --> F[Longitudinal Pilot]
    F --> G{Continuity sustained?}
    G -- No --> E
    G -- Yes --> H[Multi-human Pilot]
    H --> I{Security / Privacy / Ops ready?}
    I -- No --> J[HOLD]
    I -- Yes --> K[Productized Beta]
```

---

# Map 09｜Node Dependency Backbone

```mermaid
flowchart TB
    HOME --> FOCUS
    FOCUS --> STUDIO
    STUDIO --> ARTIFACTS
    ARTIFACTS --> REVIEW
    REVIEW --> STUDIO
    REVIEW --> MAP
    MAP --> STUDIO
    KNOWLEDGE --> FOCUS
    KNOWLEDGE --> REVIEW
    COMPARE --> STUDIO
    COMPARE --> HISTORY
    ARTIFACTS --> HISTORY
    REVIEW --> HISTORY
    SESSION[SESSION KERNEL] -.orchestrates.-> HOME
    SESSION -.orchestrates.-> STUDIO
    SESSION -.orchestrates.-> ARTIFACTS
    PEOPLE[PEOPLE / AUTHORITY] --> SESSION
    INTEGRATIONS --> ARTIFACTS
    HEALTH[SYSTEM HEALTH] --> SESSION
```
