import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse


async def register_user(db: AsyncSession, payload: RegisterRequest) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        id=uuid.uuid4(),
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def authenticate_user(db: AsyncSession, payload: LoginRequest) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return user


def issue_tokens(user_id: uuid.UUID) -> TokenResponse:
    subject = str(user_id)
    return TokenResponse(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )


def refresh_access_token(refresh_token: str) -> TokenResponse:
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    subject = payload["sub"]
    return TokenResponse(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )