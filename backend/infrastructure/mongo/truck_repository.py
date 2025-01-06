from typing import List

from bson import ObjectId

from application.responses import TruckResponse
from application.truck.truck_repository import AbstractTruckRepository
from domain.exceptions import InvalidIdError, EntityNotFoundError
from domain.truck import Truck
from infrastructure.mongo.mongo_client import MongoDBClient


class TruckRepositoryMongo(AbstractTruckRepository):
    def __init__(self):
        self.truck_collection = MongoDBClient.get_collection("trucks")

    async def upload_truck_to_db(self, truck: Truck) -> TruckResponse:
        truck_data = truck.model_dump()
        truck_data["id"] = str(self.truck_collection.insert_one(truck_data).inserted_id)
        return TruckResponse(**truck_data)

    def get_truck_by_id(self, truck_id: str) -> TruckResponse:
        try:
            object_id = ObjectId(truck_id)
        except Exception as err:
            raise InvalidIdError(truck_id, str(err))
        truck_data = self.truck_collection.find_one({"_id": object_id})

        if not truck_data:
            raise EntityNotFoundError("Truck", truck_id)

        truck_data["id"] = str(truck_data["_id"])

        return TruckResponse(**truck_data)

    def get_trucks_by_warehouse(self, warehouse_id: str) -> List[TruckResponse]:
        try:
            ObjectId(warehouse_id)
        except Exception as err:
            raise InvalidIdError(warehouse_id, str(err))

        trucks_data = self.truck_collection.find({"warehouses": warehouse_id})

        response = []
        for truck in trucks_data:
            truck["id"] = str(truck["_id"])
            response.append(TruckResponse(**truck))

        return response