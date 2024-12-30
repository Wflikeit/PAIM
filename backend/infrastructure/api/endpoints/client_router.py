from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request

from application.client.client_service import ClientService
from domain.client import Client
from infrastructure.containers import Container

router = APIRouter()


@router.post("/register")
@inject
async def upload_client(
    request: Request,
    client_service: ClientService = Depends(Provide[Container.client_service]),
):
    data = await request.form()
    client = Client(**data)
    return client_service.register_client(client)


@router.get("/clients/{client_id}")
@inject
async def get_client(
    client_id: str,
    client_service: ClientService = Depends(Provide[Container.client_service]),
):
    return client_service.get_client(client_id)
