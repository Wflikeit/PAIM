from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.order.order_service import OrderService
from application.responses import OrderResponse
from domain.order import Order
from infrastructure.containers import Container

router = APIRouter()


@router.post("/purchase", response_model=OrderResponse)
@inject
async def add_order_endpoint(
    order: Order,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderResponse:
    return order_service.add_order(order)


@router.get("/orders/{order_id}", response_model=dict)
@inject
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"order": order_service.get_order_by_id(order_id)}


@router.get("/orders", response_model=dict)
@inject
async def get_all_orders(
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"orders": order_service.get_orders()}


@router.get("/orders/{order_id}/complete", response_model=dict)
@inject
async def set_order_status_complete(
    order_id: str,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"order": order_service.mark_order_as_complete(order_id)}
