from bson import ObjectId

from application.client.client_repository import AbstractClientRepository
from application.requests import ClientResponse
from domain.client import Client
from domain.exceptions import ClientNotFoundError
from infrastructure.mongo.mongo_client import MongoDBClient


class ClientRepositoryMongo(AbstractClientRepository):
    def __init__(self):
        self.db = MongoDBClient.get_database("shop_db")

    def register_client_db(self, client: Client) -> ClientResponse:
        client_dict = client.model_dump(by_alias=True)
        client_collection = self.db["clients"]
        client_data = client.model_dump()
        client_data["id"] = str(client_collection.insert_one(client_dict).inserted_id)
        return ClientResponse(**client_data)

    def get_client_db(self, client_id: str) -> ClientResponse:
        client_collection = self.db["clients"]
        client_data = client_collection.find_one({"_id": ObjectId(client_id)})

        if not client_data:
            raise ClientNotFoundError(client_id)
        client_data["id"] = str(client_data["_id"])

        return ClientResponse(**client_data)
