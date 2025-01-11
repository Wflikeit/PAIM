from datetime import datetime
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.auth.auth_service import AuthService
from application.order.order_service import OrderService
from application.responses import OrderResponse, OrderSummaryForRegionResponse
from domain.order import Order
from infrastructure.containers import Container

order_router = APIRouter()


@order_router.post("/purchase", response_model=OrderResponse)
@inject
async def add_order_endpoint(
    order: Order,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderResponse:
    return order_service.add_order(order)


@order_router.get(
    "/orders/stats",
    dependencies=[Depends(AuthService.is_admin)],
    response_model=List[OrderSummaryForRegionResponse],
)
@inject
async def admin_stats(
    start_date: datetime,
    end_date: datetime,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> List[OrderSummaryForRegionResponse]:
    return order_service.get_orders_report_for_period(start_date, end_date)


@order_router.get("/orders/{order_id}", response_model=dict)
@inject
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"order": order_service.get_order_by_id(order_id)}


@order_router.get("/orders", response_model=dict)
@inject
async def get_all_orders(
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"orders": order_service.get_orders()}


@order_router.get("/orders/{order_id}/complete", response_model=dict)
@inject
async def set_order_status_complete(
    order_id: str,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"order": order_service.mark_order_as_complete(order_id)}


@order_router.get("/checkout", response_model=dict)
@inject
async def get_unavailable_dates(
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> dict:
    return {"dates": order_service.get_list_of_unavailable_dates()}
