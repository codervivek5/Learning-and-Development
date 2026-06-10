# app/services/auth_service.py
from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    """Service coordinates authentication and user creation."""

    @staticmethod
    async def authenticate_user(
            db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def signup_user(
            db: AsyncSession,
            user_in: UserCreate
    ) -> User:

        result = await db.execute(
            select(User).where(User.email == user_in.email)
        )

        existing_user = result.scalars().first()

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(
            str(user_in.password)
        )

        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role=user_in.role,
        )

        db.add(db_user)

        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    def generate_tokens(user_id: int) -> str:
        return create_access_token(subject=user_id)