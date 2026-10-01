1. High-Level Architecture Diagram
Code
                         +-----------------------------+
                         |        platform_core        |
                         |  (shared library: auth,     |
                         |   config, logging, cli)     |
                         +--------------+--------------+
                                        |
                                        |
        +-------------------------------+-------------------------------+
        |                                                               |
        v                                                               v
+-----------------------+                               +-----------------------+
|   platform_services   |                               |         apps          |
|  (microservices)      |                               |  (applications)       |
+-----------+-----------+                               +-----------+-----------+
            |                                                           |
            |                                                           |
            v                                                           v
+-----------------------+                               +-----------------------+
|   auth-gateway        |                               |   web_insights        |
|   (validate user)     |                               |   (web app)           |
+-----------------------+                               +-----------------------+
            |
            v
+-----------------------+                               +-----------------------+
|   data-proxy          |                               |   batch-reports       |
|   (query data)        |                               |   (scheduled jobs)    |
+-----------------------+                               +-----------------------+
            |
            v
+-----------------------+
|   telemetry           |
|   (log events)        |
+-----------------------+


2. Component Breakdown


2.1 platform_core (Shared Library)

This is the “substrate” of the platform.
Every service and app depends on it.

Includes:
Authentication middleware  
Extracts X-User and X-Tenant

Configuration system  
Provides AppSettings

Logging utilities  
Tenant-aware logging

Internal CLI  
Developer tools

Purpose:
Enforce consistency

Reduce duplication

Provide shared behavior

Enable multi‑tenant logic

2.2 platform_services (Microservices)

Each service is independent and deployable on its own.

Auth Gateway
Validates user and tenant.

Data Proxy
Executes SQL-like queries and returns mock or real data.

Telemetry
Records events for observability.

Key Characteristics:
Stateless

FastAPI-based

Communicate via HTTP

Easy to scale horizontally

2.3 apps (Applications)

Web Insights
A FastAPI web application that:

Validates user via Auth Gateway

Queries data via Data Proxy

Sends events to Telemetry

Logs per tenant

Batch Reports
A scheduled job system that:

Runs periodic tasks

Queries Data Proxy

Sends telemetry events

Logs per tenant

3. Multi-Tenant Model
The platform uses a simple but powerful tenant model based on headers:

Code
X-User: <username>
X-Tenant: <tenant-id>
Flow:
Middleware extracts tenant/user

Stored in request.state

Used for:

Logging

Routing

Data access

Telemetry

Benefits:
No complex identity provider needed

Easy to test

Easy to extend

Works across all services

4. Inter-Service Communication
All communication is done via HTTP using httpx.AsyncClient.

Example:
python
await client.get("http://localhost:8001/validate")
await client.post("http://localhost:8002/query", json={...})
await client.post("http://localhost:8003/log", json={...})
Why HTTP?
Simple

Observable

Easy to mock

Works locally and in production

Allows independent scaling

5. Logging & Observability
Logging is tenant-aware:

Code
get_logger(app_name, tenant)
Example log:

Code
2026-10-01 12:00 - web_insights.people-analytics - INFO - Fetching insights
Telemetry service receives events such as:

insights_fetched

batch_report_generated

This enables:

Monitoring

Auditing

Debugging

Usage analytics

6. Request Flow Diagram
Web Insights Request Flow
Code
Client
  |
  v
Web Insights (middleware extracts tenant/user)
  |
  v
Auth Gateway (validate user)
  |
  v
Data Proxy (fetch data)
  |
  v
Telemetry (log event)
  |
  v
Response to client
Batch Reports Flow
Code
Scheduler
  |
  v
Batch Reports
  |
  v
Data Proxy (fetch data)
  |
  v
Telemetry (log event)
  |
  v
Logs stored per tenant

7. Design Principles
Modularity
Each service is independent.

Shared Substrate
Common logic lives in platform_core.

Multi-Tenant
Tenant extracted at middleware level.

Simplicity
No unnecessary complexity.

Scalability
Each service can scale horizontally.

Observability
Telemetry + logging everywhere.

🏁 Final Notes
The architecture is:

Clean

Modular

Scalable

Multi-tenant

Easy to deploy

Easy to extend

Perfect for interviews and real-world use

