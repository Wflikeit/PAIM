from pydantic import BaseModel

class Upload_product_request(BaseModel):
    name: str
    price: float
    country_of_origin: str
    description: str
    fruit_or_vegetable: str
    file: UploadFile
    expiry_date: str
