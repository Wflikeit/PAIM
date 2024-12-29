from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File, Form

from application.product.product_service import ProductService
from infrastructure.containers import Container
from domain.product import Product

router = APIRouter()


@router.post("/upload")
@inject
async def upload_product_endpoint(
    name: str = Form(...),
    price: float = Form(...),
    country_of_origin: str = Form(...),
    description: str = Form(...),
    fruit_or_vegetable: str = Form(...),
    expiry_date: str = Form(...),
    file: UploadFile = File(...),
    product_service: ProductService = Depends(Provide[Container.product_service]),
):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPEG files are allowed")

    product_data = Product(
        name=name,
        price=price,
        country_of_origin=country_of_origin,
        description=description,
        fruit_or_vegetable=fruit_or_vegetable,
        expiry_date=expiry_date,
        file=file,
    )

    return await product_service.upload_product(product_data)


@router.get("/products/{product_id}")
@inject
async def get_product(
    product_id: str,
    product_service: ProductService = Depends(Provide[Container.product_service]),
):
    return product_service.get_product(product_id)


@router.get("/products/{product_id}/image")
@inject
async def get_product_image(
    product_id: str,
    product_service: ProductService = Depends(Provide[Container.product_service]),
):
    return product_service.get_image(product_id)
