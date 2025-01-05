from datetime import date
from typing import List

from application.client.client_repository import AbstractClientRepository
from application.order.order_repository import AbstractOrderRepository
from application.responses import OrderResponse, WarehouseResponse
from application.warehouse.warehouse_repository import AbstractWarehouseRepository
from domain.order import Order


def calculate_total_weight(products: List[dict]) -> float:
    total = 0
    for product in products:
        total += product["quantity"]
    return total


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        client_repo: AbstractClientRepository,
        warehouse_repo: AbstractWarehouseRepository,
    ):
        self._warehouse_repo = warehouse_repo
        self._order_repo = order_repo
        self._client_repo = client_repo

    def add_order(self, order: Order) -> OrderResponse:
        order_data = order.model_dump()
        order_data["warehouses"] = [self.check_warehouses(order_data["products"])]
        total_weight = calculate_total_weight(order_data["products"])
        order_data["trucks"] = [
            (self.assign_trucks(total_weight, order_data["delivery_date"]))
        ]

        order_from_db = self._order_repo.add_order(Order(**order_data))
        order_from_db_data = order_from_db.model_dump()
        self._client_repo.add_order_to_client_db(
            order_from_db_data["id"], order_from_db_data["email"]
        )
        return OrderResponse(**order_from_db_data)

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        return self._order_repo.get_order(order_id)

    def get_orders(self) -> List[OrderResponse]:
        return self._order_repo.get_all_orders()

    def get_warehouses_that_meets_demad(
        self, warehouses: List[WarehouseResponse], order_products: List[dict]
    ) -> dict:
        warehouse_availability = {}
        for warehouse in warehouses:
            warehouse_data = warehouse.model_dump()
            warehouse_availability[warehouse_data["id"]] = []
            for product in order_products:
                if (
                    product["quantity"]
                    <= warehouse_data["product_quantities"][product["product_id"]]
                ):
                    warehouse_availability[warehouse_data["id"]].append(
                        product["product_id"]
                    )
            warehouse_availability[warehouse_data["id"]] = len(
                warehouse_availability[warehouse_data["id"]]
            )
        return warehouse_availability

    def check_warehouses(self, order_products: List[dict]) -> str:
        warehouses = self._warehouse_repo.get_warehouses()
        warehouse_availability = self.get_warehouses_that_meets_demad(
            warehouses, order_products
        )

        max_len = 0
        max_len_warehouse_id = ""
        for warehouse_id in warehouse_availability.keys():
            if len(order_products) == warehouse_availability[warehouse_id]:
                return warehouse_id
            elif warehouse_availability[warehouse_id] > max_len:
                max_len = warehouse_availability[warehouse_id]
                max_len_warehouse_id = warehouse_id

        return max_len_warehouse_id

    def assign_trucks(self, total_weight: float, delivery_date: date) -> str:
        return ""
