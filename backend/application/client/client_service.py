from typing import Optional, Dict

from application.client.client_repository import AbstractClientRepository
from domain.client import Client
from domain.exceptions import ClientNotFoundError


class ClientService:
    def __init__(self, client_repo: AbstractClientRepository) -> None:
        self._client_repo = client_repo

    def register_client(self, client_data: Client) -> Optional[Dict[str, str]]:
        client_id = self._client_repo.register_client_db(client_data)

        return {
            "info": f"Client '{client_data.email}' registered successfully",
            "client_id": client_id,
        }

    def get_client(self, client_id: str) -> Optional[Dict[str, dict]]:
        client_data = self._fetch_client_data(client_id)
        return {"client": Client(**client_data).model_dump()}

    def _fetch_client_data(self, client_id: str) -> dict:
        """Retrieve raw client data from the repository."""
        client = self._client_repo.get_client_db(client_id)
        if not client:
            raise ClientNotFoundError(client_id)

        return client
