from fastapi import (APIRouter,Depends,Form,HTTPException,status,)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.admin import AdminResponse
from app.api.deps import RoleChecker
from app.schemas.user import UserResponse
from app.core.security import get_password_hash
from app.core.constants import (UserRole,CreateUserRole)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# ============================================================
# SUPER ADMIN -> CREATE ADMIN
# ============================================================
@router.post(
    "/create-admin",
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        RoleChecker(
            [UserRole.SUPER_ADMIN]

        )
    )
):
    """
    Only SUPER_ADMIN can create ADMIN accounts.
    """

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    db_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role=UserRole.ADMIN.value,
        is_active=True,
    )

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return {
        "message": "Admin created successfully",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "role": db_user.role,
        }
    }


# ============================================================
# ADMIN / SUPER_ADMIN -> CREATE USER
# ============================================================

@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    role: CreateUserRole = Form(...),

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        RoleChecker(
            [
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN
            ]
        )
    )
):
    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    db_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role=role.value,
        is_active=True,
    )

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "role": db_user.role,
        }
    }

# ============================================================
# LIST ALL ADMINS
# ============================================================

@router.get("/admins")
async def list_admins(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        RoleChecker(
            [
                UserRole.SUPER_ADMIN
            ]
        )
    )
):
    """
    List all admin users.
    Only SUPER_ADMIN can access.
    """

    # Fetch all users who have ADMIN role from database
    result = await db.execute(
        select(User).where(
            User.role == UserRole.ADMIN.value
        )
    )

    admins = result.scalars().all()

    # Convert ORM User objects into safe response format
    # (prevents leaking sensitive fields like hashed_password)
    def to_admin_response(user: User) -> AdminResponse:
        return AdminResponse(
            id=user.id,
            role=user.role,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active
        )

    # Transform all admin records into safe DTOs (Data Transfer Objects)
    admins = [to_admin_response(a) for a in admins]

    return {
        "count": len(admins),
        "admins": admins
    }


# ============================================================
# LIST ALL USERS
# ============================================================
@router.get("/users",response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        RoleChecker(
            [
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN
            ]
        )
    )
):
    """
    List all users.
    """

    result = await db.execute(select(User))

    users = [
        u for u in result.scalars().all()
        if u.role not in [
            UserRole.ADMIN.value,
            UserRole.SUPER_ADMIN.value
        ]
    ]

    return users

# ============================================================
# DEACTIVATE/ACTIVATE ADMIN
# ============================================================
@router.patch("/admins/{admin_id}/status")
async def change_admin_status(
    admin_id: int,
    is_active: bool,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(
        RoleChecker(
            [UserRole.SUPER_ADMIN]
        )
    )
):
    result = await db.execute(
        select(User).where(User.id == admin_id)
    )

    admin = result.scalars().first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    if admin.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=400,
            detail="Selected user is not an admin"
        )
    # Prevent deactivating yourself
    if admin.id == current_user.id and not is_active:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account"
        )

    admin.is_active = is_active

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    return {
        "message": f"Admin {'activated' if is_active else 'deactivated'} successfully",
        "admin_id": admin.id,
        "is_active": admin.is_active
    }


# ============================================================
# DEACTIVATE/ACTIVATE USER
# ============================================================

@router.patch("/users/{user_id}/status")
async def change_user_status(
    user_id: int,
    is_active: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        RoleChecker(
            [
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN
            ]
        )
    )
):
    """
    Activate / Deactivate User
    """

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Optional Safety
    if user.role in [
        UserRole.ADMIN.value,
        UserRole.SUPER_ADMIN.value,
    ]:
        raise HTTPException(
            status_code=400,
            detail="Use admin status endpoint for admin accounts"
        )

    user.is_active = is_active

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return {
        "message": f"User {'activated' if is_active else 'deactivated'} successfully",
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

# ============================================================
# DELETE ADMIN
# ============================================================
@router.delete("/admins/{admin_id}")
async def delete_admin(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(
        RoleChecker(
            [UserRole.SUPER_ADMIN]
        )
    )
):
    """
    Delete Admin
    Only SUPER_ADMIN can delete admins.
    """

    result = await db.execute(
        select(User).where(User.id == admin_id)
    )
    admin = result.scalars().first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    if admin.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=400,
            detail="Selected user is not an admin"
        )

    # Prevent deleting yourself
    if admin.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete yourself"
        )

    await db.delete(admin)
    await db.commit()

    return {
        "message": "Admin deleted successfully",
        "deleted_admin_id": admin_id
    }

# ============================================================
# DELETE USER
# ============================================================
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        RoleChecker(
            [
                UserRole.SUPER_ADMIN,
                # UserRole.ADMIN
            ]
        )
    )
):
    """
    Only SUPER_ADMIN can delete users.
    """

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role in [
        UserRole.ADMIN.value,
        UserRole.SUPER_ADMIN.value
    ]:
        raise HTTPException(
            status_code=400,
            detail="Use admin endpoint for admin accounts"
        )

    await db.delete(user)
    await db.commit()

    return {
        "message": "User deleted successfully"
    }