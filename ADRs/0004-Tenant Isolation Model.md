# ADR 0004: Tenant Isolation Model

## Context
The platform will serve ~5 consuming teams initially, with plausible growth to ~25 teams within two years.  
Teams build internal “insight apps” that vary significantly: interactive web apps, scheduled batch jobs, and data‑driven tools.  
One early tenant, the People Analytics team, handles highly sensitive compensation data. Their compliance partner will review the platform design before onboarding.

Given the small size of the platform team (2–3 engineers), the isolation model must:
- protect sensitive data  
- prevent accidental cross‑tenant access  
- remain simple to operate  
- support fast onboarding  
- avoid heavy multi‑tenant infrastructure that would exceed the time and staffing constraints

## Decision
We will implement **logical tenant isolation** enforced through:
1. **Tenant identity propagation** (per‑app configuration + middleware)
2. **Scoped data access** via the `data-proxy` service
3. **Scoped auth** via the `auth-gateway` service
4. **Telemetry isolation** (per‑tenant log/metric namespaces)
5. **PII scrubbing** in shared logging middleware
6. **Operator access controls** (audited and restricted)

This model provides strong isolation guarantees without requiring physical multi‑tenant infrastructure.

---

## Isolation Layers

### 1. Tenant Identity Propagation
Each app declares its tenant identity in a small configuration file:
```yaml
tenant: people-analytics