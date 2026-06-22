from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.admin import Admin
from app.core.security import verify_password
from app.core.admin_jwt_handler import create_admin_token
from app.schemas.admin_auth_schema import AdminLoginRequest


async def authenticate_admin(db: AsyncSession, payload: AdminLoginRequest) -> Admin:
    result = await db.execute(select(Admin).where(Admin.username == payload.username))
    admin = result.scalar_one_or_none()

    if not admin or not verify_password(payload.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
        )

    return admin


def issue_admin_token(admin_id) -> dict:
    return {"access_token": create_admin_token(str(admin_id)), "token_type": "bearer"}