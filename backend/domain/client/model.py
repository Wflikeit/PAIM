from pydantic import BaseModel

class Client(BaseModel):
    email: str
    payment_address: str
    delivery_address: str
    nip: str
    orders: str
    password: str
    company_name: str
