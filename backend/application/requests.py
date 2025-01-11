from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr

from domain.address import Address


class ProductRequest(BaseModel):
    name: str
    price: float
    country_of_origin: str
    description: str
    is_vegetable: bool
    expiry_date: datetime
    file: Optional[UploadFile] = None


class ClientRequest(BaseModel):
    email: EmailStr
    payment_address: Address
    delivery_address: Address
    nip: str
    password: str
    company_name: str

