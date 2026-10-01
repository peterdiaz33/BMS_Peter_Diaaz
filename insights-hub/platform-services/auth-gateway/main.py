# platform-services/auth-gateway/main.py

from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="Auth Gateway Service")

@app.get("/validate")
async def validate(request: Request):
    """
    Simple token validation stub.
    In a real system, this would validate JWTs or SSO tokens.
    """

    user = request.headers.get("X-User")
    tenant = request.headers.get("X-Tenant")

    if not user or not tenant:
        raise HTTPException(status_code=401, detail="Invalid or missing auth headers")

    return {
        "status": "validated",
        "user": user,
        "tenant": tenant
    }
