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


class ClientResponse(BaseModel):
    id: str
    email: str
    payment_address: str
    delivery_address: str
    nip: str
    orders: str
    company_name: str
