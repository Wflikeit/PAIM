from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request

from application.client.client_service import ClientService
from application.requests import ClientResponse
from domain.client import Client
from infrastructure.containers import Container

router = APIRouter()


@router.post("/register", response_model=ClientResponse)
@inject
async def upload_client(
    request: Request,
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> ClientResponse:
    data = await request.form()
    client = Client(**data)
    return client_service.register_client(client)


@router.get("/clients/{client_id}", response_model=ClientResponse)
@inject
async def get_client(
    client_id: str,
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> ClientResponse:
    return client_service.get_client(client_id)
