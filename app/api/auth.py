# app/api/auth.py
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

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
        db: AsyncSession = Depends(get_db),
):
    """
    Register a new user directly into the single central system.
    """
    allowed_roles = [
        UserRole.LEARNER,
        UserRole.DESIGNER,
        UserRole.DEVELOPER,
    ]
    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to register with the specified role."
        )

    user_in = UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        role=role,
    )
    try:
        user = await AuthService.signup_user(db=db, user_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login_custom(
        request: Request,
        username: Optional[str] = Form(None, description="OAuth2 Compatibility (Email)"),
        password: Optional[str] = Form(None, description="Account password"),
        db: AsyncSession = Depends(get_db),
):
    """
    Unified Hybrid Login Endpoint:
    1. Shows interactive fields on Swagger UI (Fixes the empty box issue).
    2. Seamlessly parses raw JSON from React UI.
    3. Fully supports Swagger's top-right Authorize Lock button via 'username'.
    """
    final_email = username
    final_password = password

    # Check if the incoming request is raw JSON from React UI
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            final_email = body.get("email")
            final_password = body.get("password")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not parse JSON authentication payload correctly."
            )

    if not final_email or not final_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email/Username and password fields are strictly required."
        )

    user = await AuthService.authenticate_user(
        db=db, email=final_email, password=final_password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = AuthService.generate_tokens(user.id)

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
