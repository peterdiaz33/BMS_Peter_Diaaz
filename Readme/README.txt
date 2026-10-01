Insights Hub — Modular Platform for Internal Services and Applications
Insights Hub is a modular, multi‑tenant platform designed to support internal services, web applications, and scheduled batch processes. It follows modern architectural patterns with clear separation between shared core logic, independent microservices, and consumer applications.

This repository contains:

A shared core library

Multiple FastAPI microservices

Web and batch applications

Architectural documentation (ADRs)

Onboarding and operational guides

## Project Structure
Code
C:\Github\BMS_Peter_Diaaz
│
├── ADRs/                     → Architectural Decision Records
├── onboarding.md             → Onboarding guide
│
├── platform_core/            → Shared internal library
│   ├── auth/                 → Authentication middleware
│   ├── config/               → Application/service configuration
│   ├── observability/        → Logging utilities
│   └── cli/                  → Internal CLI
│
├── platform_services/        → Independent FastAPI microservices
│   ├── auth-gateway/         → User & tenant validation
│   ├── data-proxy/           → SQL-like data proxy
│   └── telemetry/            → Event logging service
│
├── apps/                     → Applications consuming the services
│   ├── web_insights/         → Web application (FastAPI)
│   └── batch-reports/        → Scheduled batch jobs
│
└── README.md                 → This file
## Requirements
Install dependencies:

Code
pip install fastapi uvicorn httpx apscheduler typer
Python version:

Code
Python 3.10+
## Running the Microservices
Auth Gateway (port 8001)
Code
uvicorn platform_services.auth-gateway.main:app --port 8001
Data Proxy (port 8002)
Code
uvicorn platform_services.data-proxy.main:app --port 8002
Telemetry Service (port 8003)
Code
uvicorn platform_services.telemetry.main:app --port 8003
Each service is independent and can be started separately.

## Running the Web Insights Application
Code
uvicorn apps.web_insights.main:app --port 9001
Example request:
Code
GET /insights
Headers:
  X-User: peter
  X-Tenant: people-analytics
The app will:

Validate the user via auth-gateway

Query data via data-proxy

Send telemetry events

Log activity per tenant

## Running Batch Reports
Code
python apps/batch-reports/main.py
The batch process:

Runs every 10 seconds

Fetches data from data-proxy

Sends telemetry events

Logs activity per tenant

Demonstrates scheduled background processing
##  Authentication & Tenant Model
The platform uses a lightweight multi‑tenant model based on HTTP headers:

Code
X-User: <username>
X-Tenant: <tenant-id>
The middleware in platform_core/auth/middleware.py:

Extracts tenant and user

Stores them in request.state

Makes them available to all endpoints

Enables multi‑tenant logging and routing
##  Inter‑Service Communication
All apps communicate with services using httpx.AsyncClient.

Example:

python
await client.get("http://localhost:8001/validate")
await client.post("http://localhost:8002/query", json={...})
await client.post("http://localhost:8003/log", json={...})
This ensures:

Loose coupling

Clear separation of responsibilities

Easy scaling and replacement of services

## Documentation
ADRs/
Contains architectural decisions such as:

Service boundaries

Core library design

Multi‑tenant model

Logging strategy

onboarding.md
Explains how new developers can start working with the platform.