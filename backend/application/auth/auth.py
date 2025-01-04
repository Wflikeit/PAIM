from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pymongo import MongoClient
from fastapi import HTTPException, status

from infrastructure.mongo.mongo_client import MongoDBClient


SECRET_KEY = "your_secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


admin_collection = MongoDBClient.get_collection("admins")
client_collection = MongoDBClient.get_collection("clients")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, role: str = None, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Include role in the token payload if provided
    if role:
        to_encode.update({"role": role})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def authenticate_user(email: str, password: str):
    # Check in Admin collection
    admin_user = admin_collection.find_one({"email": email})
    if admin_user and verify_password(password, admin_user["password"]):
        return {"email": admin_user["email"], "role": "admin"}

    # Check in Client collection
    client_user = client_collection.find_one({"email": email})
    if client_user and verify_password(password, client_user["password"]):
        return {"email": client_user["email"]}

    # If not found in either collection
    return None

def generate_token_for_user(user: dict) -> str:
    # Generate a token with role information for admins
    return create_access_token(data={"sub": user["email"]}, role=user.get("role"))


def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        return {"email": email, "role": role}
    except JWTError:
        raise credentials_exception

def is_admin(user: dict):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user is not an admin",
        )
    return user
