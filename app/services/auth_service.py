# app/services/auth_service.py

import uuid
from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user import UserCreate


class AuthService:
    """Service coordinates authentication and user/organization creation."""

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
            db: AsyncSession, user_in: UserCreate
    ) -> Tuple[User, Organization]:
        # Check if user already exists
        result = await db.execute(select(User).where(User.email == user_in.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise ValueError("Email already registered")

        # Resolve or create Organization (Tenant)
        organization_id = user_in.organization_id
        organization = None

        if organization_id:
            organization = await db.get(Organization, organization_id)
            if not organization:
                raise ValueError("Tenant organization not found")
        else:
            # Create a new organization
            org_name = user_in.organization_name or f"{user_in.full_name}'s Org"
            org_slug = org_name.lower().replace(" ", "-").replace("/", "-")

            # Check slug uniqueness
            slug_res = await db.execute(
                select(Organization).where(Organization.slug == org_slug)
            )
            if slug_res.scalars().first():
                org_slug = f"{org_slug}-{uuid.uuid4().hex[:6]}"

            organization = Organization(
                name=org_name,
                slug=org_slug,
            )
            db.add(organization)
            await db.commit()
            await db.refresh(organization)

        # 🔴 CHANGE/FIX: Explicitly force cast password to string to prevent Pydantic SecretStr object reference from leaking into bcrypt
        raw_password_string = str(user_in.password)
        hashed_password = get_password_hash(raw_password_string)

        # Create new User
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role=user_in.role,
            organization_id=organization.id,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user, organization

    @staticmethod
    def generate_tokens(user_id: int) -> str:
        return create_access_token(subject=user_id)