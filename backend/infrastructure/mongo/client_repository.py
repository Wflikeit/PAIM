from bson import ObjectId

from application.client.client_repository import AbstractClientRepository
from application.responses import ClientResponse
from domain.client import Client
from domain.exceptions import ClientNotFoundError, InvalidIdError
from infrastructure.mongo.mongo_client import MongoDBClient


class ClientRepositoryMongo(AbstractClientRepository):
    def __init__(self):
        self.client_collection = MongoDBClient.get_collection("clients")

    def register_client_db(self, client: Client) -> ClientResponse:
        client_data = client.model_dump()
        client_data["id"] = str(
            self.client_collection.insert_one(client_data).inserted_id
        )
        return ClientResponse(**client_data)

    def get_client_db(self, client_id: str) -> ClientResponse:
        try:
            object_id = ObjectId(client_id)
        except Exception as err:
            raise InvalidIdError(client_id, str(err))
        client_data = self.client_collection.find_one({"_id": object_id})

        if not client_data:
            raise ClientNotFoundError(client_id)

        client_data["id"] = str(client_data["_id"])

        return ClientResponse(**client_data)
