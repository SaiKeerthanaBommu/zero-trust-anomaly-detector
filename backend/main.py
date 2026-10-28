"""Backend service sitting behind the NGINX zero-trust edge.

NGINX validates the JWT before a request ever reaches these endpoints.
The /auth/token route is only for local demos so you can mint test tokens.
"""
import os
import time

import jwt
from fastapi import FastAPI, Header, HTTPException
from prometheus_client import make_asgi_app

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 900

app = FastAPI(title="Protected Backend")
app.mount("/metrics", make_asgi_app())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/token")
def issue_token(username: str, role: str = "user"):
    """Demo-only token issuer. Replace with a real IdP in production."""
    now = int(time.time())
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + TOKEN_TTL_SECONDS,
        "jti": f"{username}-{now}",
    }
    return {"access_token": jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)}


@app.get("/api/data")
def get_data(x_user: str | None = Header(default=None)):
    """x-user is set by NGINX after it validates the token."""
    return {"message": "protected data", "user": x_user}


@app.get("/api/admin")
def admin(x_user: str | None = Header(default=None), x_role: str | None = Header(default=None)):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="admin role required")
    return {"message": "admin data", "user": x_user}
