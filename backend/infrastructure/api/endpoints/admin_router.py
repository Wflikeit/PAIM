from datetime import datetime

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from application.auth.auth_service import AuthService
from application.order.order_service import OrderService
from infrastructure.containers import Container

admin_router = APIRouter()
