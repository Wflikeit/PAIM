from fastapi import APIRouter, Depends, HTTPException, status, Request
from jwt import decode, InvalidTokenError
from path.to.MongoDBClient import MongoDBClient

router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Get MongoDB database and users collection
db = MongoDBClient.get_database("your_database_name")
users_collection = db["users"]

def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: missing token",
        )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: invalid token",
            )
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: user not found",
            )
        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: invalid token",
        )


def is_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user is not an admin",
        )
    return user


@router.get("/")
async def admin_home(user: dict = Depends(is_admin)):
    return {"message": f"Welcome, {user['email']}! You are viewing the Admin Page."}


@router.get("/stats")
async def admin_stats(user: dict = Depends(is_admin)):
    stats = {
        "users": users_collection.count_documents({}),
        "products": db["products"].count_documents({}),
    }
    return stats
