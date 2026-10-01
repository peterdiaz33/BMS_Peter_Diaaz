# platform-services/data-proxy/main.py

from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="Data Proxy Service")

@app.post("/query")
async def query(request: Request):
    """
    Stubbed data access service.
    Enforces tenant-level access rules.
    """

    tenant = request.headers.get("X-Tenant")
    if not tenant:
        raise HTTPException(status_code=401, detail="Missing tenant identity")

    body = await request.json()
    sql = body.get("sql", "SELECT * FROM stub")

    # Stubbed enforcement: People Analytics gets special handling
    if tenant == "people-analytics" and "compensation" in sql.lower():
        raise HTTPException(status_code=403, detail="Access to compensation data is restricted")

    return {
        "tenant": tenant,
        "query": sql,
        "data": [{"id": 1, "value": "stubbed-data"}]
    }
