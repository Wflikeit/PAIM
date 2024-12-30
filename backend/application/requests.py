from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    country_of_origin: str
    description: str
    fruit_or_vegetable: str
    expiry_date: str
    file: str
