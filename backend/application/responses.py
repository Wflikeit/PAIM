from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field


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
    delivery_date: str
    amount: float
    products: List[dict]
    delivery_address: str
    order_status: str
    email: EmailStr
    trucks: Optional[List[str]]
    warehouses: Optional[List[str]]
    route_length: float


class AddressResponse(BaseModel):
    id: str
    voivodeship: str
    county: str
    city: str
    street: str
    house_number: int
    postal_code: str


class WarehouseResponse(BaseModel):
    id: str
    address: str
    product_quantities: dict
    trucks: List[str] = Field(default_factory=list)
