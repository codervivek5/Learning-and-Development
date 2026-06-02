from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import Token, UserLogin
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
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Hybrid Endpoint: Dynamically parses JSON from React UI or
    Form-Data/URL-Encoded formats from Swagger UI seamlessly.
    """
    content_type = request.headers.get("content-type", "")
    email = None
    password = None

    try:
        if "application/json" in content_type:
            # Parses JSON structure from React cleanly
            body = await request.json()
            email = body.get("email")
            password = body.get("password")
        else:
            # Parses urlencoded Form structure from Swagger Authorize / Curl fields
            form_data = await request.form()
            # Standard OAuth2 form structure uses 'username' field for email mapping
            email = form_data.get("username") or form_data.get("email")
            password = form_data.get("password")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not parse authentication payload properties correctly."
        )

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email and password fields are strictly required."
        )

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
    form_data: OAuth2PasswordRequestForm = Depends(),  # For Swagger UI Authorize Box
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2 compatible form data token login.
    Keeps native Swagger UI 'Authorize' locks fully operational.
    """
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