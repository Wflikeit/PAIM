import datetime
from typing import List

from bson import ObjectId

from application.order.order_repository import AbstractOrderRepository
from application.responses import OrderResponse
from domain.entities import Entity
from domain.order import Order
from domain.exceptions import InvalidIdError, EntityNotFoundError, InvalidDateType
from infrastructure.mongo.mongo_client import MongoDBClient


class OrderRepositoryMongo(AbstractOrderRepository):
    def __init__(self):
        self.order_collection = MongoDBClient.get_collection("orders")

    def add_order(self, order: Order) -> OrderResponse:
        order_data = order.model_dump()
        order_data["id"] = str(self.order_collection.insert_one(order_data).inserted_id)
        return OrderResponse(**order_data)

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        try:
            object_id = ObjectId(order_id)
        except Exception as err:
            raise InvalidIdError(Entity.order.value, str(err))
        order_data = self.order_collection.find_one({"_id": object_id})

        if not order_data:
            raise EntityNotFoundError(Entity.order.value, order_id)

        order_data["id"] = str(order_data["_id"])
        if isinstance(order_data["delivery_date"], datetime.datetime):
            order_data["delivery_date"] = order_data["delivery_date"].replace(
                tzinfo=datetime.timezone.utc
            )
        else:
            raise InvalidDateType(order_data["delivery_date"], Entity.order.value)
        return OrderResponse(**order_data)

    def get_all_orders(self) -> List[OrderResponse]:
        orders = list(self.order_collection.find())

        response_list = []
        for order in orders:
            order["id"] = str(order["_id"])
            if isinstance(order["delivery_date"], datetime.datetime):
                order["delivery_date"] = order["delivery_date"].replace(
                    tzinfo=datetime.timezone.utc
                )
            else:
                raise InvalidDateType(order["delivery_date"], Entity.order.value)
            response_list.append(OrderResponse(**order))

        return response_list

    def update_order_status_db(self, order_id: str, status: str) -> bool:
        try:
            object_id = ObjectId(order_id)
        except Exception as err:
            raise InvalidIdError(Entity.order.value, str(err))
        result = self.order_collection.update_one(
            {"_id": object_id},
            {"$set": {"order_status": status}},
        )

        return result.acknowledged
