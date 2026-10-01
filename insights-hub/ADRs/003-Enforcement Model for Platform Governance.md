# ADR 0003: Enforcement Model for Platform Governance
## Peter Frank Diaz Rosales

## Context
The platform will serve ~5 consuming teams initially, growing to ~25 within two years.  
Teams vary significantly: some build interactive web apps, others scheduled batch jobs.  
All teams rely on shared behaviors: authentication, authorization, data access, logging, metrics, and deployment conventions.

Given the small size of the platform team (2–3 engineers), governance must be:
- lightweight to operate  
- strong enough to ensure consistency  
- predictable for tenant teams  
- enforceable without manual policing  

The enforcement model determines **where platform rules live** and **how they are applied** across all apps.

## Decision
We will use a **multi-layer enforcement model** combining:

1. **Scaffolding (CLI)**
2. **Static enforcement (linting + formatting)**
3. **CI enforcement (build rules + tests)**
4. **Runtime enforcement (shared services + middleware)**
5. **Convention-based governance (documented expectations)**

This layered approach ensures consistency without introducing heavy operational overhead.

---

## Enforcement Layers

### 1. Scaffolding (CLI)
The CLI (`platform create-app <name>`) enforces:
- folder structure  
- baseline configuration  
- logging and metrics wiring  
- auth and data access middleware  
- dependency versions  
- platform-core integration  

This ensures all apps start from a compliant baseline.

**Why here?**  
Scaffolding is the earliest point of influence and prevents divergence before it begins.

---

### 2. Static Enforcement (Linting + Formatting)
We enforce:
- code style (Black/Prettier)  
- import conventions  
- forbidden patterns (e.g., direct warehouse access)  
- required modules (auth, logging, config)

Static rules run locally and in CI.

**Why here?**  
Static checks catch violations early and cheaply.

---

### 3. CI Enforcement (Build Rules + Tests)
CI enforces:
- platform-core version compatibility  
- required tests for auth/data/logging wiring  
- dependency integrity  
- no direct calls to sensitive data sources  
- no removal of required middleware

CI is the final gate before merging.

**Why here?**  
CI ensures consistency across teams and prevents accidental regressions.

---

### 4. Runtime Enforcement (Shared Services + Middleware)
Runtime rules include:
- token validation via `auth-gateway`  
- controlled data access via `data-proxy`  
- telemetry forwarding to `telemetry` service  
- PII scrubbing in logs  
- tenant isolation checks

Runtime enforcement protects sensitive data and ensures operational consistency.

**Why here?**  
Runtime is the only place where certain rules (auth, data access, telemetry) can be guaranteed.

---

### 5. Convention-Based Governance
Documented conventions in:
- `ONBOARDING.md`  
- `README.md`  
- ADRs  

Conventions cover:
- naming  
- deployment workflow  
- logging expectations  
- error handling patterns  
- upgrade process

**Why here?**  
Not all rules need hard enforcement; some are best handled through clear documentation.

---

## Alternatives Considered

### 1. Pure CI Enforcement
**Pros**
- Strong guarantees  
- Centralized governance

**Cons**
- Too rigid  
- High friction for teams  
- Hard to maintain with 2–3 engineers

### 2. Pure Runtime Enforcement
**Pros**
- Strong protection for sensitive data  
- Centralized logic

**Cons**
- Too late in the lifecycle  
- Does not prevent structural divergence  
- Harder to debug violations

### 3. Convention-Only Model
**Pros**
- Very lightweight  
- Easy to adopt

**Cons**
- No guarantees  
- High risk of drift  
- Weak governance for sensitive teams (e.g., People Analytics)

---

## Consequences

### Positive
- Strong governance with low operational overhead  
- Predictable behavior across all apps  
- Early detection of violations  
- Runtime protection for sensitive data  
- Clear upgrade story  
- Consistent developer experience

### Negative
- Requires maintaining CLI + lint rules + CI templates  
- Some teams may prefer more autonomy  
- Runtime services introduce minimal complexity (acceptable trade-off)

---

## Deliberate Omissions
We intentionally exclude:
- heavy policy engines (OPA, Kyverno)  
- complex multi-stage CI pipelines  
- strict per-team isolation policies  
- dynamic policy evaluation at runtime  

These would be triggered by:
- scale beyond 25 teams  
- external-facing applications  
- regulatory requirements demanding stronger isolation  
- need for multi-cloud or hybrid governance

---

## Status
Accepted.
