from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.file_storage import upload_resume

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse,
    ProfilePictureResponse,
)
from app.services.auth_service import (
    register_user,
    authenticate_user,
    issue_tokens,
    refresh_access_token,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, payload)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload)
    return issue_tokens(user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest):
    return refresh_access_token(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/profile-picture", response_model=ProfilePictureResponse)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    file_bytes = await file.read()

    upload_result = upload_resume(file_bytes, file.filename)

    current_user.profile_picture_url = upload_result["url"]
    db.add(current_user)
    await db.commit()

    return ProfilePictureResponse(profile_picture_url=upload_result["url"])