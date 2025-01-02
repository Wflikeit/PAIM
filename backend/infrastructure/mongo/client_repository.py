import gridfs
from bson import ObjectId

from application.client.client_repository import AbstractClientRepository
from domain.client import Client
from infrastructure.mongo.mongo_client import MongoDBClient


class ClientRepositoryMongo(AbstractClientRepository):
    def __init__(self):
        self.db = MongoDBClient.get_database("client")
        self.fs = gridfs.GridFS(self.db)

    def register_client_db(self, client: Client) -> str:
        client_dict = client.model_dump(by_alias=True)
        client_collection = self.db["clients"]
        client_id = client_collection.insert_one(client_dict).inserted_id
        return str(client_id)

    def get_client_db(self, client_id: str) -> Client:
        client_collection = self.db["clients"]
        client = client_collection.find_one({"_id": ObjectId(client_id)})
        return client
