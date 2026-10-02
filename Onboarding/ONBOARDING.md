# Insights Hub Platform — Onboarding Guide
# Peter Frank Diaz Rosales

Welcome to the Insights Hub platform.  
This document explains how teams can build, run, and maintain applications using the shared platform substrate.

It covers:
- Platform architecture overview
- How to create a new app
- How to run platform services
- How tenant identity works
- How to use platform-core
- How to call shared services
- How to send telemetry
- How to update platform-core
- Local development workflow
- Deployment expectations
- Rules and restrictions

---

# 1. Platform Architecture Overview

The platform consists of three main components:

## 1.1 Platform Core (`platform-core`)
A shared library providing:
- Authentication middleware (stub)
- Data access stubs
- Logging and metrics
- Configuration loader
- CLI for scaffolding apps

Apps import `platform-core` directly.

## 1.2 Shared Platform Services (`platform-services`)
Three lightweight services:

### `auth-gateway`
Validates user identity and tenant identity.

### `data-proxy`
Centralized data access service enforcing tenant-level rules.

### `telemetry`
Collects logs and metrics, storing them in per-tenant namespaces.

## 1.3 Tenant Applications (`apps/`)
Two example apps:
- `web-insights` (FastAPI web app)
- `batch-reports` (APScheduler batch job)

Teams will build similar apps.

---

# 2. Creating a New Application

Apps are created using the platform CLI.

From the project root:

```bash
python -m platform_core.cli.main platform create-app my-app



##This Generates
apps/my-app/
  main.py

## The scaffold includes:

FastAPI app

Auth middleware

Config loader

Logging setup

Health endpoint

Teams can extend this structure.

3. Running Platform Services Locally
Each service runs independently.

Open three terminals:

Terminal 1 — auth-gateway
bash
uvicorn platform-services.auth-gateway.main:app --port 8001
Terminal 2 — data-proxy
bash
uvicorn platform-services.data-proxy.main:app --port 8002
Terminal 3 — telemetry
bash
uvicorn platform-services.telemetry.main:app --port 8003
All apps depend on these services.

4. Running Tenant Applications
4.1 Web App (web-insights)
bash
uvicorn apps.web-insights.main:app --port 9001
4.2 Batch App (batch-reports)
bash
python apps/batch-reports/main.py
Batch apps do not use FastAPI.

5. Tenant Identity
Every request must include:

Code
X-User: <username>
X-Tenant: <tenant-name>
Examples:

people-analytics

sales-insights

finance-ops

Tenant identity is used by:

Auth middleware

Data-proxy

Telemetry collector

Logging

Apps must propagate tenant identity in all outbound requests.

6. Using Platform Core

6.1 Auth Middleware
python
from platform_core.auth.middleware import AuthMiddleware
Applied via FastAPI middleware.

6.2 Configuration
python
from platform_core.config.settings import AppSettings
settings = AppSettings()
Supports environment variables with prefix INSIGHTS_.

6.3 Logging
python
logger = get_logger(settings.app_name, tenant)
logger.info("message")
Logs are tenant-scoped.

7. Calling Shared Services

7.1 Auth Gateway
python
await client.get(
    "http://localhost:8001/validate",
    headers={"X-User": user, "X-Tenant": tenant}
)

7.2 Data Proxy
python
await client.post(
    "http://localhost:8002/query",
    json={"sql": "SELECT * FROM insights"},
    headers={"X-Tenant": tenant}
)

7.3 Telemetry
python
await client.post(
    "http://localhost:8003/log",
    json={"event": "insights_fetched"},
    headers={"X-Tenant": tenant}
)

8. Updating Platform Core
Apps depend on platform-core.

To update:

Pull latest changes

Update imports if needed

Run the CLI update command (future enhancement)

Test locally

Platform-core uses semantic versioning.

9. Local Development Workflow
Typical workflow:

Start platform services

Start your app

Make requests with tenant headers

Check logs and telemetry

Commit changes

Push to GitHub

Example request:

bash
curl -H "X-User: peter" -H "X-Tenant: people-analytics" http://localhost:9001/insights
10. Rules and Restrictions
10.1 Forbidden
Direct access to data sources

Removing auth middleware

Removing telemetry calls

Accessing compensation data directly

Impersonating users

Removing tenant identity propagation

10.2 Required
Tenant identity in all requests

Logging for all operations

Telemetry events for key actions

Using data-proxy for all data access

Using auth-gateway for validation

11. Deployment Expectations
Teams must:

Deploy apps independently

Use platform-core as a dependency

Use shared services in production

Follow tenant isolation rules

Follow enforcement rules (ADR 0003)

12. Troubleshooting
Missing tenant headers
→ 401 Unauthorized

Accessing restricted data
→ 403 Forbidden

Telemetry not showing
→ Check headers and service port

Batch app not running
→ Ensure APScheduler installed

13. Contact
Platform Team
Insights Hub
Engineering Department

