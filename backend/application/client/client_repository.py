import abc

from application.responses import ClientResponse
from domain.client import Client


class AbstractClientRepository(abc.ABC):
    @abc.abstractmethod
    def register_client_db(self, client: Client) -> ClientResponse:
        pass

    @abc.abstractmethod
    def get_client_db(self, client_id: str) -> ClientResponse:
        pass
