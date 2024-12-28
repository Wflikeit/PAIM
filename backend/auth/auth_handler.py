import os

import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from infrastructure.mongo.mongo_client import MongoDBClient
from domain import client
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

SECRET_KEY = f"{secret_key}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter()

# Get MongoDB database and clients collection
db = MongoDBClient.get_database("your_database_name")
clients_collection = db["clients"]

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_client(email: str):
    client_data = clients_collection.find_one({"email": email})
    if client_data:
        return client(**client_data)  # Convert MongoDB document to a Client model instance
    return None

def authenticate_client(email: str, password: str):
    client = get_client(email)
    if not client:
        return False
    if not verify_password(password, client.password):
        return False
    return client

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    client = get_client(email)
    if client is None:
        raise credentials_exception
    return client

async def get_current_active_client(current_client: Client = Depends(get_current_client)):
    return current_client
