import abc
from typing import List

from application.responses import OrderResponse
from domain.order import Order


class AbstractOrderRepository(abc.ABC):
    @abc.abstractmethod
    def add_order(self, order_data: Order) -> OrderResponse:
        pass

    @abc.abstractmethod
    def get_order(self, order_id: str) -> OrderResponse:
        pass

    @abc.abstractmethod
    def get_all_orders(self) -> List[OrderResponse]:
        pass
