Overview
This document describes the logical data model for Insights Hub: the entities, relationships, and how data will be stored and accessed in a multi‑tenant environment.

Currently, data-proxy returns mock data, but the model below is designed for a future real database (PostgreSQL, SQL Server, etc.).

1. Core Entities

1. Tenant

Fields:

tenant_id (PK)

name

description

Purpose: Represents a team, department, or customer.

2. User

Fields:

user_id (PK)

username

email

tenant_id (FK → Tenant)

Purpose: Represents a person using the platform.

3. Insight

Fields:

insight_id (PK)

tenant_id (FK → Tenant)

title

category

value

created_at

Purpose: Represents a metric, KPI, or analytic result.

4. Report

Fields:

report_id (PK)

tenant_id (FK → Tenant)

name

status

generated_at

Purpose: Represents a batch-generated report.

5. TelemetryEvent

Fields:

event_id (PK)

tenant_id (FK → Tenant)

user_id (FK → User, nullable)

event_type

payload (JSON)

created_at

Purpose: Represents logged events for observability.

2. Relationships
Tenant 1‑N User

Tenant 1‑N Insight

Tenant 1‑N Report

Tenant 1‑N TelemetryEvent

User 1‑N TelemetryEvent (optional)

This ensures strict tenant isolation: all data is tied to a tenant_id.


3. Example Table Definitions (SQL)
Tenant

sql
CREATE TABLE tenants (
  tenant_id      VARCHAR(64) PRIMARY KEY,
  name           VARCHAR(255) NOT NULL,
  description    TEXT
);
User

sql
CREATE TABLE users (
  user_id        SERIAL PRIMARY KEY,
  username       VARCHAR(255) NOT NULL,
  email          VARCHAR(255),
  tenant_id      VARCHAR(64) REFERENCES tenants(tenant_id)
);
Insight

sql
CREATE TABLE insights (
  insight_id     SERIAL PRIMARY KEY,
  tenant_id      VARCHAR(64) REFERENCES tenants(tenant_id),
  title          VARCHAR(255),
  category       VARCHAR(128),
  value          NUMERIC,
  created_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
Report

sql
CREATE TABLE reports (
  report_id      SERIAL PRIMARY KEY,
  tenant_id      VARCHAR(64) REFERENCES tenants(tenant_id),
  name           VARCHAR(255),
  status         VARCHAR(64),
  generated_at   TIMESTAMP
);
TelemetryEvent

sql
CREATE TABLE telemetry_events (
  event_id       SERIAL PRIMARY KEY,
  tenant_id      VARCHAR(64) REFERENCES tenants(tenant_id),
  user_id        INTEGER REFERENCES users(user_id),
  event_type     VARCHAR(128),
  payload        JSONB,
  created_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
📡 4. Tenant-Aware Queries
Fetch insights for a tenant:

sql
SELECT *
FROM insights
WHERE tenant_id = :tenant_id;
Fetch reports for a tenant:

sql
SELECT *
FROM reports
WHERE tenant_id = :tenant_id
ORDER BY generated_at DESC;
Fetch telemetry for a tenant:

sql
SELECT *
FROM telemetry_events
WHERE tenant_id = :tenant_id
AND created_at > NOW() - INTERVAL '7 days';


5. Multi-Tenant Data Isolation

Rules:

Every table that holds business data must include tenant_id.

All queries from data-proxy must filter by tenant_id.

Batch jobs must always run per tenant, not globally.

No cross‑tenant joins without explicit design.

6. Evolution Path
Current:

data-proxy returns mock JSON.

Future:

Connect data-proxy to a real DB.

Implement tenant-aware queries.

Add indexes on tenant_id and created_at.

Add materialized views for heavy reports.