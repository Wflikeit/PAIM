from application.client.client_repository import AbstractClientRepository
from application.responses import ClientResponse
from domain.client import Client


class ClientService:
    def __init__(self, client_repo: AbstractClientRepository) -> None:
        self._client_repo = client_repo

    def register_client(self, client_data: Client) -> ClientResponse:
        return self._client_repo.register_client_db(client_data)

    def get_client(self, client_id: str) -> ClientResponse:
        return self._client_repo.get_client_db(client_id)

    # Is this needed?
    # def _fetch_client_data(self, client_id: str) -> Client:
    #     """Retrieve raw client data from the repository."""
    #     client = self._client_repo.get_client_db(client_id)
    #     if not client:
    #         raise ClientNotFoundError(client_id)
    #
    #     return client
