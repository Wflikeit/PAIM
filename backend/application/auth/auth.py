from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from infrastructure.mongo.mongo_client import MongoDBClient
# import logging
#
# # Set up logging
# logging.basicConfig(
#     level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler()  # Log to the console
#         # You can add a FileHandler here to log to a file
#     ],
# )
# logger = logging.getLogger(__name__)


SECRET_KEY = "your_secret_key"
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

    if role:
        to_encode.update({"role": role})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email: str, password: str):
    admin_user = admin_collection.find_one({"email": email})
    if admin_user and verify_password(password, admin_user["password"]):
        return {"email": admin_user["email"], "role": "admin"}

    client_user = client_collection.find_one({"email": email})
    if client_user and verify_password(password, client_user["password"]):
        return {"email": client_user["email"], "role": "client"}

    return None

def generate_token_for_user(user: dict) -> str:
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def is_admin(token: str = Depends(oauth2_scheme)):
    # logger = logging.getLogger("is_admin")

    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden: user is not an admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        # Decode the JWT token

        # logger.debug(f"Decoded token payload: {payload}")

        # Check the role in the payload
        role = payload.get("role")
        if role != "admin":
            # logger.warning("Access denied: User is not an admin")
            raise credentials_exception

        # Log successful admin access
        # logger.info("Access granted: User is an admin")
        return payload
    except JWTError as e:
        # logger.error(f"Invalid token: {str(e)}")
        raise credentials_exception
