# ADR 0002: Platform Substrate Form
# Peter Frank Diaz Rosales
## Context
The platform must support ~5 consuming teams today and plausibly ~25 within two years.  
Teams build internal “insight apps” with shared needs: authentication, authorization, access to shared data sources, deployment workflows, logging, and basic observability.

The platform team consists of 2–3 engineers who must maintain, upgrade, and support everything they build.  
Given this scale and staffing, the substrate must be simple to operate, easy to upgrade, and consistent across all tenant applications.

The substrate must support two types of workloads:
- interactive web applications
- scheduled batch jobs

It must also satisfy early requirements from the People Analytics team, whose compensation data is the most sensitive in the organization.

## Decision
We will implement the platform substrate as a **combination of three components**:

1. **Shared Library (`platform-core`)**  
   A reusable library providing:
   - authentication and authorization stubs  
   - data connection stubs (warehouse, REST API)  
   - logging and metrics (OpenTelemetry local)  
   - configuration loading  
   - common error handling  
   - a CLI for scaffolding new apps

2. **Shared Platform Services (`platform-services`)**  
   Lightweight services that centralize cross‑cutting concerns:
   - `auth-gateway` (SSO stub + token validation)  
   - `data-proxy` (controlled access to shared data sources)  
   - `telemetry` (log/metric collector)

3. **Scaffold / CLI Tooling**  
   A CLI command (`platform create-app <name>`) that:
   - generates a new tenant application  
   - applies platform conventions automatically  
   - wires in auth, data access, logging, and config  
   - ensures consistent folder structure