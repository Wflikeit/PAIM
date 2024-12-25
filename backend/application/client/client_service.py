from typing import Optional

from fastapi import HTTPException, status

from application.client.client_repository import AbstractClientRepository
from domain.client import Client


class ClientService:
    def __init__(self, client_repo: AbstractClientRepository) -> None:
        self._client_repo = client_repo

    def register_client(self, client_data: Client):

        client_id = self._client_repo.register_client_db(client_data)

        return {
            "info": f"Client '{client_data.email}' registered successfully",
            "client_id": client_id,
        }

    def get_client(self, client_id: str) -> Optional[dict]:
        client = self._client_repo.get_client_db(client_id)
        client_info = {}

        if client:
            client_info = {
                "email": client["email"],
                "payment_address": client["payment_address"],
                "delivery_address": client["delivery_address"],
                "nip": client["nip"],
                "orders": client["orders"],
                "password": client["password"],
                "company_name": client["company_name"],
            }

        if not client_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        return {"client": client_info}
