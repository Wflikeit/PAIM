from datetime import date
from typing import List

from application.client.client_repository import AbstractClientRepository
from application.order.order_repository import AbstractOrderRepository
from application.responses import OrderResponse, WarehouseResponse
from application.truck.truck_repository import AbstractTruckRepository
from application.warehouse.warehouse_repository import AbstractWarehouseRepository
from domain.order import Order


def calculate_total_weight(products: List[dict]) -> float:
    total = 0
    for product in products:
        total += product["quantity"]
    return total


def get_warehouses_that_meets_demand(
        warehouses: List[WarehouseResponse], order_products: List[dict],
) -> List[dict]:
    each_warehouse_with_demanded_products = []
    for warehouse in warehouses:
        warehouse_availability = {}
        warehouse_data = warehouse.model_dump()
        warehouse_id = warehouse_data["id"]
        warehouse_availability[warehouse_id] = []

        for product in order_products:
            quantity = warehouse_data["product_quantities"]
            product_id = product["product_id"]
            if product["quantity"] <= quantity[product_id]:
                warehouse_availability[warehouse_id].append(product_id)
        each_warehouse_with_demanded_products.append(warehouse_availability)
    return each_warehouse_with_demanded_products


def subtract_products_from_order(order_products: List[dict], products_in_warehouse: List[dict]) -> List[dict]:
    new_order_products_data = []
    for order in order_products:
        for product_id in order.keys():
            for product_in_warehouse in products_in_warehouse:
                product_in_warehouse_id = list(product_in_warehouse.keys())[0]
                if product_id == product_in_warehouse_id:
                    quantity = order[product_id] - product_in_warehouse[product_in_warehouse_id]
                    new_order_products_data.append({product_id: quantity})
    return new_order_products_data


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        client_repo: AbstractClientRepository,
        warehouse_repo: AbstractWarehouseRepository,
        trucks_repo: AbstractTruckRepository
    ):
        self._warehouse_repo = warehouse_repo
        self._order_repo = order_repo
        self._client_repo = client_repo
        self._truck_repo = trucks_repo

    def add_order(self, order: Order) -> OrderResponse:
        order_data = order.model_dump()
        delivery_date = order_data["delivery_date"]
        total_weight = calculate_total_weight(order_data["products"])
        order_data["warehouses"], order_data["trucks"] = self.check_warehouses(order_data["products"], total_weight, delivery_date)

        order_from_db = self._order_repo.add_order(Order(**order_data))
        order_from_db_data = order_from_db.model_dump()
        order_id = order_from_db_data["order_id"]
        order_email = order_from_db_data["email"]

        self._client_repo.add_order_to_client_db(order_id, order_email)
        return OrderResponse(**order_from_db_data)

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        return self._order_repo.get_order(order_id)

    def get_orders(self) -> List[OrderResponse]:
        return self._order_repo.get_all_orders()

    def check_warehouses(self, order_products: List[dict], total_weight: float, delivery_date: str) -> tuple[str,List[str]]:
        warehouses = self._warehouse_repo.get_warehouses()
        warehouse_availability = get_warehouses_that_meets_demand(warehouses, order_products)

        sorted_warehouses = sorted(warehouse_availability,
                                   key=lambda item: len(next(iter(item.values()))),
                                   reverse=True)
        assigned_trucks_memory = []
        warehouse_id = ""
        for warehouse in sorted_warehouses:
            total_weight = [total_weight]
            warehouse_id = list(warehouse.keys())[0]
            assigned_trucks = self.find_trucks_for_delivery(warehouse_id, total_weight, delivery_date)
            total_weight = total_weight[0]
            if total_weight <= 0:
                return warehouse_id, assigned_trucks
            else:
                assigned_trucks_memory += assigned_trucks
                order_products = subtract_products_from_order(order_products, warehouse[warehouse_id])
        return warehouse_id, assigned_trucks_memory

    def find_trucks_for_delivery(self, warehouse, total_weight: List[float], delivery_date: str) -> List[str]:
        total_weight = total_weight[0]
        trucks = self._truck_repo.get_trucks_by_warehouse(warehouse)
        assigned_trucks = []
        for truck in trucks:
            truck_data = truck.model_dump()
            if self.is_truck_available_at_date(truck_data["orders"], delivery_date):
                total_weight -= truck_data["lift_capacity"]
                assigned_trucks.append(truck["id"])
                if total_weight <= 0:
                    break
        return assigned_trucks

    def is_truck_available_at_date(self, orders: List[str], delivery_date: str) -> bool:
        for order in orders:
            order_data = self.get_order_by_id(order).model_dump()
            if order_data["delivery_date"] == delivery_date:
                return False
        return True

    def assign_trucks(self, total_weight, param):
        pass


