# app/api/deps.py
import uuid
from typing import Generator, Optional
from fastapi import Depends, HTTPException, Header, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import TENANT_HEADER
from app.db.session import get_db
from app.models.user import User
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Dependency that returns the current authenticated User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception

    user_id = payload["sub"]
    try:
        user_uuid = int(user_id)
    except (ValueError, TypeError):
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


def get_current_organization_id(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> int:
    """Dependency retrieving the tenant organization ID from header or auth user."""
    organization_id = getattr(request.state, "organization_id", None)

    if not organization_id:
        organization_id = current_user.organization_id

    try:
        return int(organization_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format for tenant header {TENANT_HEADER}. Must be an integer."
        )
