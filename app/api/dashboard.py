# app/api/dashboard.py
from fastapi import APIRouter, Depends

from app.api.deps import (
    get_current_user,
    RoleChecker
)

router = APIRouter()

@router.get("/super-admin")
async def super_admin_dashboard(
    current_user=Depends(
        RoleChecker(
            ["SUPER_ADMIN"]
        )
    )
):
    return {
        "dashboard": "super_admin",
        "user": current_user.email
    }

@router.get("/admin")
async def admin_dashboard(
    current_user=Depends(
        RoleChecker(
            [
                "ADMIN",
                "SUPER_ADMIN"
            ]
        )
    )
):
    return {
        "dashboard": "admin",
        "user": current_user.email
    }

@router.get("/user")
async def user_dashboard(
    current_user=Depends(
        get_current_user
    )
):
    return {
        "dashboard": "user",
        "role": current_user.role,
        "user": current_user.email
    }