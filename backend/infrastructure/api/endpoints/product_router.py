from fastapi import APIRouter, UploadFile, HTTPException, File, Form, status

from application.product.product_service import ProductService
from domain.product import Product
from infrastructure.mongo.product_repository import ProductRepositoryMongo

router = APIRouter()

repo = ProductRepositoryMongo()
product_service = ProductService(repo)
@router.post("/upload")
async def upload_product_endpoint(
    name: str = Form(...),
    price: float = Form(...),
    country_of_origin: str = Form(...),
    description: str = Form(...),
    fruit_or_vegetable: str = Form(...),
    expiry_date: str = Form(...),
    file: UploadFile = File(...),
):
    
    try:
        if file.content_type != "image/jpeg":
            raise HTTPException(status_code=400, detail="Only JPEG files are allowed")

        product_data = Product(
            name=name,
            price= price,
            country_of_origin=country_of_origin,
            description=description,
            fruit_or_vegetable=fruit_or_vegetable,
            expiry_date=expiry_date,
            file=file,
        )

        response = await product_service.upload_product(product_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}")
async def get_product_endpoint(product_id: str):
    return product_service.get_product(product_id)
        



@router.get("/products/{product_id}/image")
async def get_product_image_endpoint(product_id: str):
    return product_service.get_image(product_id)
        
