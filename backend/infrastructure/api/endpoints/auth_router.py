from application.auth.auth import authenticate_user, create_access_token, is_admin
from fastapi import APIRouter, HTTPException, status, Depends


router = APIRouter()

@router.post("/token")
async def login_for_access_token(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Admin routes
@router.get("/")
async def admin_home(user: dict = Depends(is_admin)):
    return {"message": "Welcome to the Admin Page"}

@router.get("/stats")
async def admin_stats(user: dict = Depends(is_admin)):
    stats = {"users": 100, "products": 50}
    return stats
