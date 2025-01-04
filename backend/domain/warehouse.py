from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field

from domain.address import Address
from domain.product import Product
from domain.truck import Truck


class Warehouse(BaseModel):
    address: str
    product_quantities: List[str] = Field(default_factory=list)
    trucks: List[str] = Field(default_factory=list)
