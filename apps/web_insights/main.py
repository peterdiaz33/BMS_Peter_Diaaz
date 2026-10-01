from fastapi import FastAPI, Request
import httpx

from platform_core.auth.middleware import AuthMiddleware
from platform_core.config.settings import AppSettings
from platform_core.observability.logging import get_logger

app = FastAPI(title="Web Insights App")

settings = AppSettings(app_name="web_insights")
auth_middleware = AuthMiddleware()

@app.middleware("http")
async def auth_middleware_wrapper(request: Request, call_next):
    return await auth_middleware(request, call_next)

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}

@app.get("/insights")
async def insights(request: Request):
    tenant = request.state.tenant
    user = request.state.user

    logger = get_logger(settings.app_name, tenant)
    logger.info("Fetching insights for tenant")

    async with httpx.AsyncClient() as client:
        # Call auth-gateway
        auth_resp = await client.get(
            "http://localhost:8001/validate",
            headers={"X-User": user, "X-Tenant": tenant}
        )

        # Call data-proxy
        data_resp = await client.post(
            "http://localhost:8002/query",
            json={"sql": "SELECT * FROM insights"},
            headers={"X-Tenant": tenant}
        )

        # Send telemetry
        await client.post(
            "http://localhost:8003/log",
            json={"event": "insights_fetched"},
            headers={"X-Tenant": tenant}
        )

    return {
        "tenant": tenant,
        "auth": auth_resp.json(),
        "data": data_resp.json()
    }
