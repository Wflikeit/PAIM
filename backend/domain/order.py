from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field

from domain.product_order import ProductOrder


class Order(BaseModel):
    date: date = Field(default_factory=date.today)
    amount: float
    products: List[ProductOrder] = Field(default_factory=list)
    address: str
    order_status: str
    email: EmailStr
    trucks: Optional[List[str]] = Field(default_factory=list)
    warehouses: Optional[List[str]] = Field(default_factory=list)
    route_length: float
