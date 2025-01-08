from typing import Optional

from pydantic import BaseModel, EmailStr

from application.responses import AddressResponse
from domain.address import Address


class Client(BaseModel):
    email: EmailStr
    payment_address: Address | AddressResponse
    delivery_address: Address | AddressResponse
    nip: Optional[str] = ""
    password: str
    company_name: Optional[str] = ""
