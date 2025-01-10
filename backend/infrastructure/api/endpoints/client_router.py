from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext

from application.auth.auth import AuthService
from application.client.client_service import ClientService
from application.responses import ClientResponse, SuccessfullRegisterClientResponse
from domain.client import Client
from infrastructure.api.endpoints.auth_router import admin_collection, client_collection
from infrastructure.containers import Container

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register", response_model=SuccessfullRegisterClientResponse)
@inject
async def upload_client(
    client: Client,
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> SuccessfullRegisterClientResponse:
    client.password = pwd_context.hash(client.password)

    access_token = AuthService.create_access_token(
        data={
            "email": client.email,
            "role": "client",
        }
    )

    print(access_token)

    registered_client = client_service.register_client(client).model_dump()
    registered_client["access_token"] = access_token

    return SuccessfullRegisterClientResponse(**registered_client)


@router.get("/clients/{client_id}", response_model=ClientResponse)
@inject
async def get_client(
    client_id: str,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    credentials: HTTPAuthorizationCredentials = Security(
        AuthService.security
    ),  # Add JWT authentication
) -> ClientResponse:
    # Validate that the user is an admin
    AuthService.is_admin(credentials=credentials)

    # Proceed to get client details
    return client_service.get_client(client_id)
