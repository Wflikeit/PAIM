from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext

from application.auth.auth import AuthService
from application.client.client_service import ClientService
from application.responses import ClientResponse
from domain.client import Client
from infrastructure.containers import Container

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register", response_model=ClientResponse)
@inject
async def upload_client(
    request: Client,
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> ClientResponse:
    request.password = pwd_context.hash(request.password)

    return client_service.register_client(request)


@router.get("/clients/{client_id}", response_model=ClientResponse)
@inject
async def get_client(
    client_id: str,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    credentials: HTTPAuthorizationCredentials = Security(AuthService.security),  # Add JWT authentication
) -> ClientResponse:
    # Validate that the user is an admin
    AuthService.is_admin(credentials=credentials)

    # Proceed to get client details
    return client_service.get_client(client_id)
