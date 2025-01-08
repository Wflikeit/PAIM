from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from infrastructure.mongo.mongo_client import MongoDBClient

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

admin_collection = MongoDBClient.get_collection("admins")
client_collection = MongoDBClient.get_collection("clients")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, role: str = None, fullname: str = None, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    if role:
        to_encode.update({"role": role})
    if fullname:
        to_encode.update({"fullname": fullname})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email: str, password: str):
    admin_user = admin_collection.find_one({"email": email})
    if admin_user and verify_password(password, admin_user["password"]):
        return {"email": admin_user["email"], "role": "admin", "fullname": admin_user["fullname"]}

    client_user = client_collection.find_one({"email": email})
    if client_user and verify_password(password, client_user["password"]):
        return {"email": client_user["email"], "role": "client", "fullname": client_user["fullname"]}

    return None

def generate_token_for_user(user: dict) -> str:
    print("AAAA", user.get("fullname"))
    return create_access_token(data={"sub": user["email"]}, role=user.get("role"), fullname=user.get("fullname"))

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
        fullname: str = payload.get("fullname")
        if email is None or role is None or fullname is None:
            raise credentials_exception
        return {"email": email, "role": role, "fullname": fullname}
    except JWTError:
        raise credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def is_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden: user is not an admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        fullname = payload.get("fullname")
        if role != "admin":
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
