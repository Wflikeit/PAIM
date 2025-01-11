from application.address.address_repository import AbstractAddressRepository
from application.client.client_repository import AbstractClientRepository
from application.responses import ClientResponse
from domain.address import Address
from domain.client import Client


class ClientService:
    def __init__(
        self,
        client_repo: AbstractClientRepository,
        address_repo: AbstractAddressRepository,
    ) -> None:
        self._client_repo = client_repo
        self._address_repo = address_repo

    def register_client(self, client: Client) -> ClientResponse:
        client_data = client.model_dump()
        payment_address = Address(**client_data["payment_address"])
        client_data["payment_address"] = self._address_repo.add_address(payment_address)
        delivery_address = Address(**client_data["delivery_address"])
        client_data["delivery_address"] = self._address_repo.add_address(
            delivery_address
        )
        client = Client(**client_data)
        return self._client_repo.register_client_db(client)

    def get_client(self, client_id: str) -> ClientResponse:
        return self._client_repo.get_client_db(client_id)
