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
