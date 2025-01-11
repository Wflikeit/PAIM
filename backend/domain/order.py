from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field

from domain.address import Address


class Order(BaseModel):
    delivery_date: datetime
    amount: float
    products: List[dict] = Field(default_factory=list)
    delivery_address: Address
    order_status: str
    email: EmailStr
    trucks: Optional[List[str]] = Field(default_factory=list)
    warehouses: Optional[List[str]] = Field(default_factory=list)
    route_length: float
