from typing import Optional
from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    country_of_origin: str
    description: str
    is_vegetable: bool
    expiry_date: datetime
    file: Optional[UploadFile] = None
