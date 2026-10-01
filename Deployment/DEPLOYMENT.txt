Overview
This guide explains how to deploy the Insights Hub platform in both local and production environments. The platform consists of:

platform_core (shared library)

platform_services (FastAPI microservices)

apps (web application + batch jobs)

All components are independent and can be deployed separately.

1. Deployment Architecture
Code
+---------------------------+
|        Reverse Proxy      |
|      (NGINX / Traefik)    |
+------------+--------------+
             |
             v
+---------------------------+
|   Auth Gateway (8001)     |
+---------------------------+

+---------------------------+
|   Data Proxy (8002)       |
+---------------------------+

+---------------------------+
|   Telemetry (8003)        |
+---------------------------+

+---------------------------+
|   Web Insights (9001)     |
+---------------------------+

+---------------------------+
|   Batch Reports (cron)    |
+---------------------------+
Each service runs independently and communicates via HTTP.

2. Environment Variables
Create a .env file at the root of the project:

Code
APP_ENV=production
LOG_LEVEL=INFO
DEFAULT_TENANT=people-analytics
Each service can load environment variables using os.getenv().

3. Local Deployment (Developer Mode)
Start microservices:
Code
uvicorn platform_services.auth-gateway.main:app --host 0.0.0.0 --port 8001
uvicorn platform_services.data-proxy.main:app --host 0.0.0.0 --port 8002
uvicorn platform_services.telemetry.main:app --host 0.0.0.0 --port 8003
Start Web Insights:
Code
uvicorn apps.web_insights.main:app --host 0.0.0.0 --port 9001
Start Batch Reports:
Code
python apps/batch-reports/main.py

4. Docker Deployment (Recommended)
Create a Dockerfile for each service.

Example: platform_services/auth-gateway/Dockerfile
dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ../../platform_core ./platform_core
COPY . .

RUN pip install fastapi uvicorn httpx apscheduler typer

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
Repeat for:

data-proxy

telemetry

web_insights

Build:
Code
docker build -t auth-gateway .
Run:
Code
docker run -p 8001:8001 auth-gateway

5. Docker Compose (Full Platform)
Create docker-compose.yml:

yaml
version: "3.9"

services:
  auth-gateway:
    build: ./platform_services/auth-gateway
    ports:
      - "8001:8001"

  data-proxy:
    build: ./platform_services/data-proxy
    ports:
      - "8002:8002"

  telemetry:
    build: ./platform_services/telemetry
    ports:
      - "8003:8003"

  web-insights:
    build: ./apps/web_insights
    ports:
      - "9001:9001"
Start everything:

Code
docker compose up --build

6. Reverse Proxy (Production)
Use NGINX or Traefik to expose services under clean URLs.

Example NGINX config:
nginx
server {
    listen 80;

    location /auth/ {
        proxy_pass http://auth-gateway:8001/;
    }

    location /data/ {
        proxy_pass http://data-proxy:8002/;
    }

    location /telemetry/ {
        proxy_pass http://telemetry:8003/;
    }

    location /insights/ {
        proxy_pass http://web-insights:9001/;
    }
}

7. Logging & Monitoring
Recommended tools:
Prometheus → metrics

Grafana → dashboards

ELK Stack → logs

UptimeRobot → uptime monitoring

Each service already logs per tenant using:

Code
get_logger(app_name, tenant)

8. Security Considerations
Use HTTPS (Let’s Encrypt)

Validate tenant headers

Add API keys or JWT tokens

Restrict CORS

Run services behind a firewall

Use Docker secrets for sensitive data


9. Production Testing Checklist
Before going live:

All services respond to /health

Web Insights can call all services

Batch Reports runs without errors

Logs appear in monitoring system

Reverse proxy routes correctly

No service crashes under load

Final Notes
Your platform is now ready for:

## Local development

## Docker deployment

## Production deployment

## Scaling via microservices

## Monitoring and logging

## Secure multi‑tenant operation