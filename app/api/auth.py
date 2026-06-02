from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.core.constants import UserRole

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    email: str = Form(..., description="User email address"),
    password: str = Form(..., description="Account password"),
    full_name: str = Form(..., description="Full name of the user"),
    role: UserRole = Form(UserRole.LEARNER, description="User role in the platform"),
    organization_name: Optional[str] = Form(None, description="New organization name (creates org on signup)"),
    db: AsyncSession = Depends(get_db),
):
    """Register a new user and tenant organization."""
    user_in = UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        role=role,
        organization_name=organization_name,
    )
    try:
        user, _ = await AuthService.signup_user(db=db, user_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login_custom(
    # FastAPI ka Form() multipart/form-data aur urlencoded dono handle karta hai
    email: str = Form(..., description="Registered email address"),
    password: str = Form(..., description="Account password"),
    db: AsyncSession = Depends(get_db),
):
    """Login with credentials returning access token."""
    user = await AuthService.authenticate_user(
        db=db, email=email, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = AuthService.generate_tokens(user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/access-token", response_model=Token)
async def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """OAuth2 compatible token login, for swagger documentation compatibility."""
    user = await AuthService.authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = AuthService.generate_tokens(user.id)
    return Token(access_token=access_token, token_type="bearer")
