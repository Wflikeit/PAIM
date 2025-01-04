from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field

from domain.product_order import ProductOrder


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    country_of_origin: str
    description: str
    fruit_or_vegetable: str
    expiry_date: str
    file: str


class ClientResponse(BaseModel):
    id: str
    email: str
    payment_address: str
    delivery_address: str
    nip: str
    orders: List[str] = Field(default_factory=list)
    company_name: str


class OrderResponse(BaseModel):
    id: str
    date: date
    amount: float
    products: List[ProductOrder]
    address: str
    order_status: str
    email: EmailStr
    trucks: Optional[List[str]]
    warehouses: Optional[List[str]]
    route_length: float
