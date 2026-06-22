from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.admin import Admin
from app.schemas.admin_auth_schema import AdminLoginRequest, AdminTokenResponse, AdminResponse
from app.services.admin_auth_service import authenticate_admin, issue_admin_token

router = APIRouter(prefix="/api/v1/admin-auth", tags=["admin-auth"])


@router.post("/login", response_model=AdminTokenResponse)
async def admin_login(payload: AdminLoginRequest, db: AsyncSession = Depends(get_db)):
    admin = await authenticate_admin(db, payload)
    return issue_admin_token(admin.id)


@router.get("/me", response_model=AdminResponse)
async def get_admin_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin