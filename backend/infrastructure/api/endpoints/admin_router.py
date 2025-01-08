from application.auth.auth import (
    authenticate_user,
    create_access_token,
    is_admin,
    generate_token_for_user,
)
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/", dependencies=[Depends(is_admin)])
async def admin_home():
    return {"message": "Welcome to the Admin Page"}


@router.get("/stats", dependencies=[Depends(is_admin)])
async def admin_stats():
    stats = {"users": 100, "products": 50}
    return stats
