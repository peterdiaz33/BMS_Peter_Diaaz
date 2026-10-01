Overview
This document describes the complete testing strategy for Insights Hub, including:

Unit testing

Integration testing

End‑to‑end testing

Load testing

Security testing

Tenant isolation testing

Batch job testing

The goal is to ensure reliability, correctness, and multi‑tenant safety across all services and applications.


1. Testing Frameworks
Recommended tools:

pytest → unit & integration tests

httpx.AsyncClient → API testing

pytest-asyncio → async tests

locust → load testing

OWASP ZAP → security testing

Postman → manual API validation

Install:

Code
pip install pytest pytest-asyncio httpx locust


2. Unit Testing
Unit tests focus on:

Core library functions

Middleware behavior

Logging utilities

Configuration loading

Example: Testing Auth Middleware
python
async def test_auth_middleware():
    from platform_core.auth.middleware import AuthMiddleware
    from starlette.requests import Request

    middleware = AuthMiddleware()

    scope = {
        "type": "http",
        "headers": [
            (b"x-user", b"peter"),
            (b"x-tenant", b"people-analytics")
        ]
    }

    request = Request(scope)
    await middleware.dispatch(request, lambda req: req)

    assert request.state.user == "peter"
    assert request.state.tenant == "people-analytics"

3. Integration Testing
Integration tests validate communication between:

Auth Gateway

Data Proxy

Telemetry

Web Insights

Example: Testing Web Insights → Auth Gateway
python
async def test_web_insights_auth():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:9001/insights",
            headers={
                "X-User": "peter",
                "X-Tenant": "people-analytics"
            }
        )
        assert response.status_code == 200
        assert "auth" in response.json()


4. End‑to‑End Testing
End‑to‑end tests simulate real user flows:

Scenario: Fetch Insights
Send request to Web Insights

Web Insights calls Auth Gateway

Web Insights calls Data Proxy

Web Insights calls Telemetry

Response is aggregated

Expected:
All services respond

Tenant is preserved

Logs are generated

Telemetry event is recorded



5. Batch Job Testing
Batch Reports runs every 10 seconds.

Test strategy:
Mock Data Proxy

Mock Telemetry

Validate logs

Validate job scheduling

Example:
python
async def test_batch_job(monkeypatch):
    async def mock_query(*args, **kwargs):
        return {"result": [{"id": 1}]}

    monkeypatch.setattr("httpx.AsyncClient.post", mock_query)

    from apps.batch_reports.main import generate_report
    await generate_report()


6. Security Testing
Required tests:
Missing headers

Invalid tenant

Invalid user

SQL injection attempts

Unauthorized access

Example:
python
async def test_missing_tenant():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9001/insights")
        assert response.status_code in (400, 401, 403)


7. Load Testing
Use locust.

Example locustfile:
python
from locust import HttpUser, task

class LoadTest(HttpUser):
    @task
    def insights(self):
        self.client.get(
            "/insights",
            headers={
                "X-User": "peter",
                "X-Tenant": "people-analytics"
            }
        )
Run:

Code
locust -f locustfile.py


8. Tenant Isolation Testing
Critical for multi‑tenant systems.

Tests:
Tenant A cannot access Tenant B data

Logs are separated

Telemetry is separated

Batch jobs run per tenant

Example:
python
async def test_cross_tenant_access():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8002/query",
            headers={"X-Tenant": "tenantA"},
            json={"sql": "SELECT * FROM insights WHERE tenant_id='tenantB'"}
        )
        assert response.status_code == 403


9. Testing Checklist
Before release:
All unit tests pass

All integration tests pass

All E2E tests pass

Tenant isolation validated

Batch jobs validated

Load tests show stable performance

Security tests show no vulnerabilities



Final Notes
This testing guide ensures:

Reliability

Multi‑tenant safety

Correct inter-service behavior

Secure operation

Scalable performance