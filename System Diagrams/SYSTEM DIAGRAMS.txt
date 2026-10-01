Overview
This document contains all major diagrams describing the architecture, data flow, request flow, and deployment topology of the Insights Hub platform.

All diagrams are ASCII-based so they can be viewed in any environment (GitHub, terminals, editors).

1. High-Level Architecture Diagram
Code
                         +-----------------------------+
                         |        platform_core        |
                         |  (auth, config, logging)    |
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

2. Request Flow Diagram (Web Insights)
Code
Client
  |
  v
Web Insights (FastAPI)
  |
  |-- Extract tenant/user via middleware
  |
  v
Auth Gateway (validate identity)
  |
  v
Data Proxy (fetch insights)
  |
  v
Telemetry (log event)
  |
  v
Response to client

3. Batch Job Flow Diagram (Batch Reports)
Code
Scheduler (APS)
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
Tenant-aware logging

4. Tenant Flow Diagram
Code
Request Headers:
  X-User: peter
  X-Tenant: people-analytics

        |
        v
+-----------------------------+
|   Auth Middleware           |
|   (platform_core/auth)      |
+-----------------------------+
        |
        v
request.state.user = "peter"
request.state.tenant = "people-analytics"
        |
        v
Used by:
  - Web Insights
  - Batch Reports
  - Auth Gateway
  - Data Proxy
  - Telemetry


5. Data Flow Diagram
Code
Web Insights
    |
    | SQL request
    v
Data Proxy
    |
    | Query DB (future)
    v
Database
    |
    | Results
    v
Data Proxy
    |
    | JSON response
    v
Web Insights


6. Deployment Diagram (Docker Compose)
Code
+------------------------------------------------------+
|                    Docker Host                       |
|                                                      |
|  +------------------+   +------------------+          |
|  | auth-gateway     |   | data-proxy       |          |
|  | (8001)           |   | (8002)           |          |
|  +------------------+   +------------------+          |
|                                                      |
|  +------------------+   +------------------+          |
|  | telemetry        |   | web-insights     |          |
|  | (8003)           |   | (9001)           |          |
|  +------------------+   +------------------+          |
|                                                      |
|  +------------------+                                |
|  | batch-reports    |                                |
|  | (cron job)       |                                |
|  +------------------+                                |
+------------------------------------------------------+

 7. Reverse Proxy Routing Diagram (NGINX)
Code
Client
  |
  v
NGINX Reverse Proxy
  |
  +--> /auth/      → auth-gateway:8001
  |
  +--> /data/      → data-proxy:8002
  |
  +--> /telemetry/ → telemetry:8003
  |
  +--> /insights/  → web-insights:9001

8. Component Interaction Diagram
Code
+------------------+
| Web Insights     |
+------------------+
        |
        | calls
        v
+------------------+
| Auth Gateway     |
+------------------+
        |
        | calls
        v
+------------------+
| Data Proxy       |
+------------------+
        |
        | calls
        v
+------------------+
| Telemetry        |
+------------------+


Final Notes
This document provides:

Architecture diagrams

Request flow diagrams

Batch flow diagrams

Tenant flow diagrams

Deployment diagrams

Reverse proxy routing

Component interaction diagrams