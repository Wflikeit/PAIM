from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field

from domain.address import Address


class Warehouse(BaseModel):
    address: Address
    product_quantities: dict
    trucks: List[str] = Field(default_factory=list)
