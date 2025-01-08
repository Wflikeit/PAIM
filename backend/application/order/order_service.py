from typing import List

from application.client.client_repository import AbstractClientRepository
from application.order.order_repository import AbstractOrderRepository
from application.responses import OrderResponse, WarehouseResponse
from application.truck.truck_repository import AbstractTruckRepository
from application.warehouse.warehouse_repository import AbstractWarehouseRepository
from domain.order import Order


def calculate_total_weight(products: List[dict]) -> float:
    return sum(product["quantity"] for product in products)


def get_warehouses_with_available_products(
    warehouses: List[WarehouseResponse], order_products: List[dict]
) -> List[dict]:
    """
    Find warehouses that can supply the demanded products.
    """
    warehouse_availability = []
    for warehouse in warehouses:
        available_products = {}
        warehouse_data = warehouse.model_dump()
        warehouse_id = warehouse_data["id"]

        for product in order_products:
            product_quantities = warehouse_data["product_quantities"]
            product_id = product["product_id"]
            if product_id in product_quantities and product_quantities[product_id] > 0:
                available_products[product_id] = min(
                    product_quantities[product_id], product["quantity"]
                )

        if available_products:
            warehouse_availability.append({warehouse_id: available_products})
    return warehouse_availability


def subtract_products_from_order(
    order_products: List[dict], warehouse_products: dict
) -> List[dict]:
    """Subtract products fulfilled by a warehouse from the remaining order."""
    remaining_products = []
    for product in order_products:
        product_id = product["product_id"]
        quantity_needed = product["quantity"]

        if product_id in warehouse_products:
            quantity_supplied = warehouse_products[product_id]
            if quantity_needed > quantity_supplied:
                remaining_products.append(
                    {
                        "product_id": product_id,
                        "quantity": quantity_needed - quantity_supplied,
                    }
                )
        else:
            remaining_products.append(product)

    return remaining_products


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        client_repo: AbstractClientRepository,
        warehouse_repo: AbstractWarehouseRepository,
        truck_repo: AbstractTruckRepository,
    ):
        self._warehouse_repo = warehouse_repo
        self._order_repo = order_repo
        self._client_repo = client_repo
        self._truck_repo = truck_repo

    def add_order(self, order: Order) -> OrderResponse:
        order_data = order.model_dump()
        delivery_date = order_data["delivery_date"]
        products = order_data["products"]
        total_weight = calculate_total_weight(products)

        warehouses, trucks = self.assign_warehouses_and_trucks(
            products, total_weight, delivery_date
        )

        order_data["warehouses"] = warehouses
        order_data["trucks"] = trucks

        order_from_db = self._order_repo.add_order(Order(**order_data))
        order_id = order_from_db.model_dump()["id"]
        order_data["id"] = order_id

        if not self._client_repo.add_order_to_client_db(order_id, order_data["email"]):
            raise Exception("Failed to link order to client")
        if self._truck_repo.add_order_to_truck_db(order_id, trucks) != len(trucks):
            raise Exception("Failed to link order to trucks")

        return OrderResponse(**order_data)

    def assign_warehouses_and_trucks(
        self, order_products: List[dict], total_weight: float, delivery_date: str
    ) -> tuple[List[str], List[str]]:
        warehouses = self._warehouse_repo.get_warehouses()
        available_warehouses = get_warehouses_with_available_products(
            warehouses, order_products
        )

        assigned_warehouses = []
        assigned_trucks = []
        remaining_products = order_products

        for warehouse in available_warehouses:
            warehouse_id = list(warehouse.keys())[0]
            warehouse_products = warehouse[warehouse_id]

            trucks = self.assign_trucks_for_warehouse(
                warehouse_id, remaining_products, warehouse_products
            )
            if not trucks:
                continue

            assigned_trucks.extend(trucks)
            assigned_warehouses.append(warehouse_id)
            remaining_products = subtract_products_from_order(
                remaining_products, warehouse_products
            )
            total_weight = calculate_total_weight(remaining_products)

            if total_weight == 0:
                break

        if total_weight > 0:
            raise Exception(
                "Unable to fulfill order: insufficient warehouses or trucks"
            )

        return assigned_warehouses, assigned_trucks

    def assign_trucks_for_warehouse(
        self,
        warehouse_id: str,
        order_products: List[dict],
        delivery_date: str,
    ) -> List[str]:
        trucks = self._truck_repo.get_trucks_by_warehouse(warehouse_id)
        assigned_trucks = []
        remaining_weight = calculate_total_weight(order_products)

        for truck in trucks:
            truck_data = truck.model_dump()
            truck_capacity = truck_data["lift_capacity"]

            if not self.is_available_on_date(
                truck_data["active_orders"], delivery_date
            ):
                continue

            if remaining_weight == 0:
                break

            if truck_capacity >= remaining_weight:
                assigned_trucks.append(truck_data["id"])
                return assigned_trucks

            remaining_weight -= truck_capacity
            assigned_trucks.append(truck_data["id"])

        return assigned_trucks

    def is_available_on_date(self, orders: List[str], delivery_date: str) -> bool:
        return all(
            self.get_order_by_id(order).model_dump()["delivery_date"] != delivery_date
            for order in orders
        )

    def get_order_by_id(self, order_id: str) -> OrderResponse:
        return self._order_repo.get_order_by_id(order_id)

    def get_orders(self) -> List[OrderResponse]:
        return self._order_repo.get_all_orders()

    def mark_order_as_complete(self, order_id: str) -> OrderResponse:
        if not self._order_repo.update_order_status_db(order_id, "complete"):
            raise Exception("Failed to mark order as complete")
        order = self._order_repo.get_order_by_id(order_id)
        order_data = order.model_dump()
        truck_ids = order_data["trucks"]
        modified_trucks = self._truck_repo.delete_order_from_truck_db(
            order_id, truck_ids
        )
        if modified_trucks != len(truck_ids):
            raise Exception("Failed to mark order as complete")
        return OrderResponse(**order_data)
