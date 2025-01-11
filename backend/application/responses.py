from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    country_of_origin: str
    description: str
    is_vegetable: bool
    expiry_date: datetime
    file: str


class ClientResponse(BaseModel):
    id: str
    email: EmailStr
    payment_address: str
    delivery_address: str
    nip: Optional[str] = ""
    orders: Optional[List[str]] = Field(default_factory=list)
    company_name: Optional[str] = ""


class SuccessfullRegisterClientResponse(BaseModel):
    id: str
    email: EmailStr
    payment_address: str
    delivery_address: str
    nip: Optional[str] = ""
    orders: Optional[List[str]] = Field(default_factory=list)
    company_name: Optional[str] = ""
    access_token: str


class AddressResponse(BaseModel):
    id: str
    voivodeship: str
    city: str
    street: str
    house_number: int
    postal_code: str


class OrderResponse(BaseModel):
    id: str
    delivery_date: datetime
    amount: float
    products: List[dict]
    delivery_address: str
    order_status: str
    email: EmailStr
    trucks: List[str]
    warehouses: List[str]
    route_length: float


class OrderSummaryForRegionResponse(BaseModel):
    amount: float
    region: str
    order_count: int


class WarehouseResponse(BaseModel):
    id: str
    address: str
    product_quantities: dict
    trucks: List[str] = Field(default_factory=list)


class TruckResponse(BaseModel):
    id: str
    registration_number: str
    active_orders: List[str] = Field(default_factory=list)
    warehouse: str
    lift_capacity: float
