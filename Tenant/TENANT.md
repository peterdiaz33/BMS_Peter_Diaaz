TENANT_MODEL.md — Multi‑Tenant Architecture & Design
This document explains how tenants work, how they flow through the system, how they affect logging, routing, data access, and how your platform supports multi‑tenant behavior across all services and apps.

I’ll generate it now, clean, professional, and ready to save as:

Code
C:\Github\BMS_Peter_Diaaz\TENANT_MODEL.md

TENANT_MODEL.md — Multi‑Tenant Model for Insights Hub
 Overview
Insights Hub is designed as a multi‑tenant platform, meaning multiple teams, departments, or customers can use the same infrastructure while keeping their data, logs, and operations isolated.

The tenant model is intentionally simple, lightweight, and easy to extend.

 1. Tenant Identification
Tenants are identified using HTTP headers:

Code
X-User: <username>
X-Tenant: <tenant-id>
These headers are required for:

Web Insights

Batch Reports

All microservices

Example:
Code
X-User: peter
X-Tenant: people-analytics


2. Tenant Extraction (Middleware)
Tenant extraction happens in:

Code
platform_core/auth/middleware.py
Flow:
Middleware intercepts every request

Reads X-User and X-Tenant

Stores them in request.state.user and request.state.tenant

Passes the request to the endpoint

Code Summary:
python
request.state.tenant = request.headers.get("X-Tenant", "default")
request.state.user = request.headers.get("X-User", "anonymous")
This ensures every service and app has access to tenant information.

3. Tenant Propagation Across Services
When Web Insights or Batch Reports call microservices, they forward the tenant headers:

python
headers={"X-User": user, "X-Tenant": tenant}
This ensures:

Auth Gateway validates the correct tenant

Data Proxy executes tenant-specific queries

Telemetry logs tenant-specific events

Tenant context flows through the entire system.

4. Tenant-Aware Logging
Logging uses:

Code
get_logger(app_name, tenant)
This produces logs like:

Code
2026-10-01 12:00 - web_insights.people-analytics - INFO - Fetching insights
Benefits:
Logs are grouped by tenant

Easy debugging

Easy auditing

Easy monitoring

Clear separation of tenant activity

5. Tenant-Based Data Access
Although the current Data Proxy returns mock data, the architecture supports:

Tenant-specific databases

Tenant-specific schemas

Tenant-specific query routing

Tenant-specific permissions

Example future extension:
Code
SELECT * FROM insights WHERE tenant = :tenant
The tenant model is ready for real data isolation.

6. Security Considerations
Recommended:
Validate tenant IDs in Auth Gateway

Restrict tenants to allowed users

Add API keys or JWT tokens

Prevent cross-tenant access

Log suspicious tenant activity

Example validation:
Code
if tenant not in allowed_tenants_for_user:
    return {"error": "Unauthorized tenant"}

7. Tenant Testing Scenarios
Scenario 1: Valid Tenant
Code
X-User: peter
X-Tenant: people-analytics
Expected:

Auth Gateway returns valid

Data Proxy returns data

Telemetry logs event

Web Insights aggregates response

Scenario 2: Missing Tenant
Code
(no headers)
Expected:

Tenant defaults to default

User defaults to anonymous

Logs show default tenant

Data Proxy returns default data

Scenario 3: Invalid Tenant
Code
X-Tenant: unknown-team
Expected:

Auth Gateway may reject

Data Proxy may return empty

Telemetry logs invalid tenant event

8. Design Principles Behind the Tenant Model
Simplicity
No complex identity provider required.

Consistency
Tenant flows through all layers.

Extensibility
Easy to add:

JWT

OAuth

API keys

RBAC

Database isolation

Observability
Tenant-aware logs and telemetry.

Security
Clear separation of tenant activity.

Final Notes
The tenant model is:

Lightweight

Powerful

Easy to test

Easy to extend

Fully integrated across the platform

Ready for production-grade multi‑tenant behavior