from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.db.session import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.admin_auth import router as admin_auth_router
from app.api.v1.resume import router as resume_router
from app.api.v1.company import router as company_router
from app.api.v1.interview import router as interview_router
from app.api.v1.voice import router as voice_router
from app.api.v1.report import router as report_router
from app.api.v1.analytics import router as analytics_router

app = FastAPI(
    title="AI Interview Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-interview-platform-mwgoo9vyr-shrayanskumar1.vercel.app",
        "https://ai-interview-platform-two-chi.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(admin_auth_router)
app.include_router(resume_router)
app.include_router(company_router)
app.include_router(interview_router)
app.include_router(voice_router)
app.include_router(report_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    return {"message": "API Running"}


@app.get("/health")
async def health():
    db_status = "unknown"

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print("DATABASE ERROR:", repr(e))
        db_status = f"error: {repr(e)}"

    return {
        "status": "ok",
        "environment": settings.environment,
        "database": db_status,
    }