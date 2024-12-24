from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile


class Product(BaseModel):
    name: str
    price: str
    country_of_origin: str
    description: str
    fruit_or_vegetable: str
    expiry_date: str
    file: Optional[UploadFile] = None
