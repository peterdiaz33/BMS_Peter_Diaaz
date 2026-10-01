# 001-monorepo.md: Monorepo for the Insights Hub Platform
# Peter Frank Diaz Rosales

## Context
The platform team consists of 2–3 engineers who are responsible for building, maintaining, and supporting the platform substrate and its shared components.  
The platform will serve ~5 consuming teams initially, with a plausible growth to ~25 teams within two years.  
All teams will build internal “insight apps” that share common needs: authentication, authorization, access to shared data sources, deployment workflows, and baseline observability.

Given the team size, the expected growth, and the need for consistent governance and fast onboarding, repository structure is a foundational architectural decision.

## Decision
We will use a **monorepo** to host:
- the platform substrate (`platform-core`)
- shared platform services (`platform-services`)
- example tenant applications (`apps`)
- documentation (`docs`)
- Architecture Decision Records (`ADRs`)
- tooling, scripts, and CI configuration

All components will live in a single Git repository called **insights-hub**.

## Alternatives Considered

### 1. Multi‑repo (one repo per app or per component)
**Pros**
- Clear separation of ownership per team  
- Independent versioning and release cycles  
- Familiar model for large organizations

**Cons**
- High overhead for a small platform team  
- Harder to enforce standards and conventions  
- More friction for onboarding new teams  
- Complex upgrade story when shared libraries evolve  
- Duplication of tooling and CI configuration  
- Slower iteration speed

### 2. Hybrid model (platform repo + separate app repos)
**Pros**
- Some separation of concerns  
- Platform remains centralized

**Cons**
- Still introduces versioning friction  
- Requires cross‑repo coordination  
- More cognitive load for new teams  
- Harder to guarantee consistent observability and deployment patterns

## Consequences

### Positive
- **Centralized governance**: linting, CI rules, scaffolding, and conventions are applied uniformly.  
- **Fast onboarding**: new teams clone one repo and immediately have everything they need.  
- **Simplified upgrade story**: platform-core changes propagate cleanly across all apps.  
- **Lower operational overhead**: ideal for a 2–3 engineer platform team.  
- **Shared tooling**: one place for scripts, dev environment, and documentation.  
- **Better visibility**: platform engineers can see all tenant apps and diagnose issues quickly.

### Negative
- The repository may grow large over time.  
- Requires discipline to maintain clear boundaries between modules.  
- Some teams may prefer independent repos (trade-off accepted given scale and constraints).

## Status
Accepted.
