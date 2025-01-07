from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field

from application.responses import AddressResponse
from domain.address import Address


class Client(BaseModel):
    email: EmailStr
    payment_address: Address|AddressResponse
    delivery_address: Address|AddressResponse
    nip: Optional[str] = ''
    orders: List[str] = Field(default_factory=list)
    password: str
    company_name: Optional[str] = ''
