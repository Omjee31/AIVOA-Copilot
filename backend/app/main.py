from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.audit import router as audit_router
from app.api.chat import router as chat_router
from app.api.complaints import router as complaints_router
from app.api.documents import router as documents_router
from app.core.config import settings


app = FastAPI(
    title="AIVOA Customer Complaint Copilot",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url.rstrip("/"),
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(chat_router)
app.include_router(complaints_router)
app.include_router(documents_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AIVOA Customer Complaint Copilot backend is running"}