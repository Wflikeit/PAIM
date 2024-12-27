from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.client.client_service import ClientService
from domain.client import Client
from infrastructure.containers import Container

router = APIRouter()


@router.post("/register")
@inject
async def upload_client(client_data: Client,
                        client_service: ClientService = Depends(Provide[Container.client_service])
                        ):
    return client_service.register_client(client_data)


@router.get("/clients/{client_id}")
@inject
async def get_client(
        client_id: str,
        client_service: ClientService = Depends(Provide[Container.client_service])
):
    return client_service.get_client(client_id)
