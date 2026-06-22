import uuid

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    profile_picture_url: str | None = None

    class Config:
        from_attributes = True

class ProfilePictureResponse(BaseModel):
    profile_picture_url: str