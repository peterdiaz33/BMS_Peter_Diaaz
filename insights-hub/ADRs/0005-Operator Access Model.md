# ADR 0005: Operator Access Model
# Peter Frank Diaz Rosales

## Context
The platform team consists of 2–3 engineers who are responsible for maintaining, supporting, and operating the platform substrate and shared services.  
They require visibility into system health, logs, metrics, and error traces to diagnose issues across ~5 consuming teams today and plausibly ~25 in the future.

However, one early tenant — People Analytics — handles highly sensitive compensation data.  
Their compliance partner requires strict guarantees that platform operators cannot access raw tenant data or bypass tenant-level restrictions.

The operator access model must balance:
- operational needs  
- security requirements  
- auditability  
- simplicity for a small platform team  

## Decision
We will implement a **restricted and auditable operator access model** based on:

1. **Operational visibility without data visibility**
2. **Strict separation between telemetry and raw data**
3. **Audited operator actions**
4. **Role-based operator permissions**
5. **No direct access to tenant data sources**
6. **No impersonation of tenant users**

This model ensures platform engineers can operate the system safely without accessing sensitive tenant data.

---

## Operator Capabilities

### 1. Allowed: Operational Visibility
Operators can view:
- service health dashboards  
- logs (scrubbed of PII)  
- metrics (per-tenant namespaces)  
- error traces  
- deployment status  
- platform-core version usage  
- data-proxy access logs (metadata only)

This visibility is necessary for diagnosing issues and supporting tenant teams.

---

### 2. Allowed: Platform-Level Actions
Operators can:
- restart shared services  
- deploy updates to platform-core  
- update CLI scaffolding  
- inspect CI failures  
- monitor telemetry pipelines  
- debug platform services (auth-gateway, data-proxy, telemetry)

These actions affect the platform but not tenant data.

---

### 3. Forbidden: Raw Tenant Data Access
Operators cannot:
- query tenant data directly  
- access warehouse tables  
- bypass data-proxy restrictions  
- view unredacted logs  
- retrieve request bodies containing sensitive data  
- access People Analytics compensation data

All data access must flow through tenant-scoped services.

---

### 4. Forbidden: User Impersonation
Operators cannot:
- generate tokens for tenant users  
- impersonate employees  
- bypass authentication flows  
- modify tenant identity metadata

This prevents privilege escalation and accidental exposure.

---

### 5. Auditing of Operator Actions
All operator actions are logged, including:
- service restarts  
- configuration changes  
- platform-core upgrades  
- access to telemetry dashboards  
- failed attempts to access restricted areas  
- CLI usage for platform updates

Audit logs are immutable and stored in a separate operator namespace.

---

## Enforcement Mechanisms

### 1. Runtime Enforcement
Shared services (`auth-gateway`, `data-proxy`) enforce:
- tenant boundaries  
- operator role restrictions  
- rejection of unauthorized access attempts

### 2. Telemetry Scrubbing
Logs are scrubbed of:
- names  
- emails  
- compensation values  
- identifiers  
- request bodies containing PII

Operators only see sanitized telemetry.

### 3. CI Enforcement
CI prevents:
- changes that weaken operator restrictions  
- removal of scrubbing middleware  
- direct data-source access in apps or platform-core

### 4. Documentation-Based Governance
Operator responsibilities and restrictions are documented in:
- `ONBOARDING.md`  
- `README.md`  
- ADRs  

This ensures clarity and consistency.

---

## Alternatives Considered

### 1. Full Operator Access
**Pros**
- Maximum debugging capability

**Cons**
- Unacceptable for People Analytics  
- Violates internal compliance  
- High risk of accidental exposure

### 2. Zero Operator Access
**Pros**
- Maximum security

**Cons**
- Impossible to operate the platform  
- Platform team cannot support tenants  
- Slows down incident response

### 3. Privileged Access via Break-Glass Mechanism
**Pros**
- Strong security  
- Controlled emergency access

**Cons**
- Too complex for the exercise  
- Requires additional infrastructure  
- Hard to justify for internal-only apps

---

## Consequences

### Positive
- Strong protection for sensitive data  
- Clear separation between operations and data  
- Predictable operator behavior  
- Full auditability  
- Low operational overhead  
- Acceptable for People Analytics compliance

### Negative
- Operators may have limited visibility during complex incidents  
- Scrubbing may hide useful debugging information  
- Requires discipline to maintain boundaries

---

## Deliberate Omissions
We intentionally exclude:
- break-glass access mechanisms  
- per-operator encryption keys  
- physical isolation of operator dashboards  
- multi-cloud operator access controls  

These would be triggered by:
- external-facing applications  
- regulatory requirements (SOC2, ISO27001)  
- scale beyond 25 teams  
- need for forensic-grade auditing

---

