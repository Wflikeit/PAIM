from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field

from domain.address import Address


class Client(BaseModel):
    email: str
    payment_address: Address|str
    delivery_address: Address|str
    nip: str
    orders: List[str] = Field(default_factory=list)
    password: str
    company_name: str
