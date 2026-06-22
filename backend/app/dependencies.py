import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt_handler import decode_token
from app.db.session import get_db
from app.models.user import User
from app.core.admin_jwt_handler import decode_admin_token
from app.models.admin import Admin

bearer_scheme = HTTPBearer()
admin_bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(admin_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_admin_token(token)
    if not payload:
        raise credentials_exception

    admin_id = payload.get("sub")
    if not admin_id:
        raise credentials_exception

    result = await db.execute(select(Admin).where(Admin.id == uuid.UUID(admin_id)))
    admin = result.scalar_one_or_none()

    if not admin:
        raise credentials_exception

    return admin