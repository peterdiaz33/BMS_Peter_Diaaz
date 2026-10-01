# platform-services/telemetry/main.py

from fastapi import FastAPI, Request

app = FastAPI(title="Telemetry Collector Service")

@app.post("/log")
async def log(request: Request):
    """
    Simple telemetry collector.
    Stores logs in per-tenant namespaces (stubbed).
    """

    tenant = request.headers.get("X-Tenant", "unknown")
    body = await request.json()

    # Stub: print logs to console
    print(f"[TELEMETRY] tenant={tenant} | event={body}")

    return {"status": "received", "tenant": tenant}
