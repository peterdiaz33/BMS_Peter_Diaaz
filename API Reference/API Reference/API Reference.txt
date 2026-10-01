API_REFERENCE.md — Complete API Documentation
This is essential for:

Developers

Integrators

QA testers

Future maintainers

External consumers

Below is your full, professional, production‑ready API_REFERENCE.md, ready to save as:

Code
C:\Github\BMS_Peter_Diaaz\API_REFERENCE.md

API_REFERENCE.md — Insights Hub API Reference
🔧 Overview
This document provides a complete reference for all API endpoints across the Insights Hub platform, including:

Auth Gateway

Data Proxy

Telemetry

Web Insights

Batch Reports (logical API behavior)

All endpoints follow a multi‑tenant model using:

Code
X-User: <username>
X-Tenant: <tenant-id>

1. Common Headers
All services require:

Code
X-User: <username>
X-Tenant: <tenant-id>
Content-Type: application/json
Example:

Code
X-User: peter
X-Tenant: people-analytics

2. Auth Gateway API (port 8001)
GET /validate
Validates user and tenant.

Request:

Code
GET /validate
Headers:
  X-User: peter
  X-Tenant: people-analytics
Response:

json
{
  "user": "peter",
  "tenant": "people-analytics",
  "valid": true
}
Use cases:

Identity validation

Tenant validation

Pre-check before accessing other services


3. Data Proxy API (port 8002)
POST /query
Executes a SQL-like query.

Request:

Code
POST /query
Headers:
  X-Tenant: people-analytics
Body:
{
  "sql": "SELECT * FROM insights"
}
Response (mock):

json
{
  "tenant": "people-analytics",
  "sql": "SELECT * FROM insights",
  "result": [
    { "id": 1, "value": "example" }
  ]
}
Use cases:

Fetch insights

Fetch reports

Tenant-specific queries

Batch job data retrieval

4. Telemetry API (port 8003)
POST /log
Logs an event for observability.

Request:

Code
POST /log
Headers:
  X-Tenant: people-analytics
Body:
{
  "event": "insights_fetched"
}
Response:

json
{
  "tenant": "people-analytics",
  "event": "insights_fetched"
}
Use cases:

Audit trails

Monitoring

Usage analytics

Batch job event logging

5. Web Insights API (port 9001)
GET /health
Health check.

Response:

json
{
  "status": "ok",
  "app": "web_insights"
}
GET /insights
Aggregates data from all services.

Request:

Code
GET /insights
Headers:
  X-User: peter
  X-Tenant: people-analytics
Response:

json
{
  "tenant": "people-analytics",
  "auth": { ... },
  "data": { ... }
}
Flow:

Validate user via Auth Gateway

Query insights via Data Proxy

Log event via Telemetry

Return aggregated response

6. Batch Reports (logical API behavior)
Batch Reports is not an HTTP API — it is a scheduled process.

Job: generate_report()
Runs every 10 seconds.

Actions:

Query Data Proxy

Log event via Telemetry

Write logs per tenant

Example logged event:

Code
batch_report_generated

7. Error Handling
Missing Tenant
Code
{
  "error": "Missing X-Tenant header"
}
Missing User
Code
{
  "error": "Missing X-User header"
}
Invalid SQL
Code
{
  "error": "Invalid SQL syntax"
}
Service Unavailable
Code
{
  "error": "Upstream service unavailable"
}

8. Security Requirements
All endpoints require:

Tenant header

User header

JSON payloads

No anonymous access (except health checks)

Recommended enhancements:

API keys

JWT tokens

Role-based access control

Final Notes
This API reference covers:

All microservices

All application endpoints

All tenant-aware flows

All request/response formats