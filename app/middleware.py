from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
import uuid
from fastapi.responses import JSONResponse

MAX_JSON_BYTES = 3 * 1024 * 1024  # 3MB

class MaxJSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            cl = request.headers.get("content-length")
            if cl and int(cl) > MAX_JSON_BYTES:
                raise HTTPException(status_code=413, detail="JSON too large. Use multipart/form-data instead.")
        return await call_next(request)

async def all_exceptions_handler(request: Request, exc: Exception):
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": str(exc), "correlation_id": cid}}
    )
