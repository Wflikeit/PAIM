from fastapi import APIRouter, HTTPException, status
from domain.client import Client
from application.client.client_service import ClientService
from infrastructure.mongo.client_repository import ClientRepositoryMongo

router = APIRouter()
repo = ClientRepositoryMongo()
clientService = ClientService(repo)


@router.post("/register")
async def upload_client_endpoint(client_data: Client):
    return clientService.register_client(client_data)


@router.get("/clients/{client_id}")
async def get_client_endpoint(client_id: str):
    return clientService.get_client(client_id)


