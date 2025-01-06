from typing import List

from bson import ObjectId

from application.order.order_repository import AbstractOrderRepository
from application.responses import OrderResponse
from domain.order import Order
from domain.exceptions import InvalidIdError, EntityNotFoundError
from infrastructure.mongo.mongo_client import MongoDBClient


class OrderRepositoryMongo(AbstractOrderRepository):
    def __init__(self):
        self.order_collection = MongoDBClient.get_collection("orders")

    def add_order(self, order: Order) -> OrderResponse:
        order_data = order.model_dump()
        order_data["id"] = str(self.order_collection.insert_one(order_data).inserted_id)
        return OrderResponse(**order_data)

    def get_order(self, order_id: str) -> OrderResponse:
        try:
            object_id = ObjectId(order_id)
        except Exception as err:
            raise InvalidIdError(order_id, str(err))
        order_data = self.order_collection.find_one({"_id": object_id})

        if not order_data:
            raise EntityNotFoundError("Order", order_id)

        order_data["id"] = str(order_data["_id"])

        return OrderResponse(**order_data)

    def get_all_orders(self) -> List[OrderResponse]:
        orders = list(self.order_collection.find())

        response_list = []
        for order in orders:
            order["id"] = str(order["_id"])

            response_list.append(OrderResponse(**order))

        return response_list
