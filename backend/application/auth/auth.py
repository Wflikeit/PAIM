from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from infrastructure.api.exception_handler import create_credentials_exception


class AuthService:
    secret_key = os.getenv("SECRET_KEY", "default-secret-key-for-tests")
    algorithm = "HS256"
    access_token_expire_minutes = 30
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    security = HTTPBearer()  # HTTP Bearer scheme for token-based authentication

    @staticmethod
    def verify_jwt_token(
        credentials: HTTPAuthorizationCredentials = Security(security),
    ) -> dict:
        try:
            payload = jwt.decode(
                credentials.credentials,
                AuthService.secret_key,
                algorithms=[AuthService.algorithm],
            )
            return payload  # Return the decoded payload if valid
        except JWTError:
            raise create_credentials_exception  # Handle invalid tokens

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict,
        role: Optional[str] = None,
        fullname: Optional[str] = None,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=AuthService.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        if role:
            to_encode.update({"role": role})
        if fullname:
            to_encode.update({"fullname": fullname})

        return jwt.encode(
            to_encode, AuthService.secret_key, algorithm=AuthService.algorithm
        )

    @staticmethod
    def authenticate_user(
        email: str, password: str, admin_collection, client_collection
    ):
        admin_user = admin_collection.find_one({"email": email})
        if admin_user and AuthService.verify_password(password, admin_user["password"]):
            return {
                "email": admin_user["email"],
                "role": "admin",
                "fullname": admin_user["fullname"],
            }

        client_user = client_collection.find_one({"email": email})
        if client_user and AuthService.verify_password(
            password, client_user["password"]
        ):
            return {
                "email": client_user["email"],
                "role": "client",
                "fullname": client_user["fullname"],
            }

        return None

    @staticmethod
    def generate_token_for_user(user: dict) -> str:
        return AuthService.create_access_token(
            data={"sub": user["email"]},
            role=user.get("role"),
            fullname=user.get("fullname"),
        )

    @staticmethod
    def is_admin(token: str):
        try:
            payload = jwt.decode(
                token, AuthService.secret_key, algorithms=[AuthService.algorithm]
            )
            role = payload.get("role")
            if role != "admin":
                raise create_credentials_exception
            return payload
        except JWTError:
            raise create_credentials_exception
