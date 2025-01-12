import os
from datetime import datetime
from typing import List

import stripe
from dependency_injector.wiring import inject, Provide
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from application.auth.auth_service import AuthService
from application.order.order_service import OrderService
from application.responses import OrderResponse, OrderSummaryForRegionResponse
from domain.order import Order
from infrastructure.containers import Container

order_router = APIRouter()
load_dotenv()
FRONTEND_URL = os.getenv("REACT_APP_URL")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@order_router.post("/purchase")
@inject
async def add_order_endpoint(
    order: Order,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    """
        Create a new Stripe Checkout Session and redirect the user to the session URL.
        """
    try:
        # Map products from the order into Stripe line items
        line_items = [
            {
                "price_data": {
                    "currency": "pln",  # Adjust this to your desired currency
                    "product_data": {"name": product["product_id"]},
                    "unit_amount": int(product["price"] * 100),  # Amount in cents
                },
                "quantity": product["quantity"],
           }
            for product in order.products
        ]

        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=f"{FRONTEND_URL}/success",
            cancel_url=f"{FRONTEND_URL}/checkout",
            customer_email=order.email,
        )

        # Save the order in your system
        # order_service.add_order(order)

        # Redirect to the checkout session URL
        return {"url":checkout_session.url}
    except Exception as e:
        # Return an HTTPException with a 400 status code and error message
        raise HTTPException(status_code=400, detail=str(e))



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

#! /usr/bin/env python3.6


@order_router.post('/create-checkout-session')
async def create_checkout_session():
    """
    Create a new Stripe Checkout Session and redirect the user to the session URL.
    """
    try:
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Replace '{{PRICE_ID}}' with your actual Price ID
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{FRONTEND_URL}/success",
            cancel_url=f"{FRONTEND_URL}/cancel",
        )
        # Redirect to the checkout session URL
        return RedirectResponse(url=checkout_session.url)
    except Exception as e:
        # Return an HTTPException with a 400 status code and error message
        raise HTTPException(status_code=400, detail=str(e))