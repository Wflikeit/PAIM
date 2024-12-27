from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request

router = APIRouter()

fake_users_db = {"admin@gmail.com": {"email": "admin@gmail.com", "role": "admin"}}


def get_current_user(request: Request):
    user_email = request.headers.get("X-User-Email")
    if not user_email or user_email not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: unauthorized user"
        )
    return fake_users_db[user_email]


def is_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user is not an admin"
        )
    return user


@router.get("/")
async def admin_home(user: dict = Depends(is_admin)):
    return {"message": "Welcome to the Admin Page"}


@router.get("/stats")
async def admin_stats(user: dict = Depends(is_admin)):
    stats = {"users": 100, "products": 50}
    return stats
