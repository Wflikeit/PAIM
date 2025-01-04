from typing import List

from application.client.client_repository import AbstractClientRepository
from application.order.order_repository import AbstractOrderRepository
from application.product.product_repository import AbstractProductRepository
from application.responses import OrderResponse
from domain.order import Order
from domain.product_order import ProductOrder


def calculate_total_weight(products: List[ProductOrder]) -> float:
    total = 0
    for product in products:
        total += product.quantity
    return total


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        client_repo: AbstractClientRepository,
        product_repo: AbstractProductRepository,
    ):
        self._order_repo = order_repo
        self._client_repo = client_repo
        self._product_repo = product_repo

    def add_order(self, order_data: Order) -> OrderResponse:
        self.check_warehouses(order_data)
        calculate_total_weight(order_data.products)
        self.assign_trucks(order_data)

        order = self._order_repo.add_order(order_data)
        self._client_repo.add_order_to_client_db(order.id, order.email)
        return order

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        return self._order_repo.get_order(order_id)

    def get_orders(self) -> List[OrderResponse]:
        return self._order_repo.get_all_orders()

    def check_warehouses(self, order_data):
        pass

    def assign_trucks(self, order_data):
        pass
