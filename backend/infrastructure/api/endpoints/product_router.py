from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from starlette.datastructures import FormData
from starlette.requests import Request

from application.product.product_service import ProductService
from application.requests import ProductResponse
from infrastructure.containers import Container
from domain.product import Product

router = APIRouter()


@router.post("/upload", response_model=ProductResponse)
@inject
async def upload_product_endpoint(
        request: Request,
        product_service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductResponse:
    data = await request.form()
    file = data["file"]

    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPEG files are allowed")

    product = Product(**data)
    return await product_service.upload_product(product)


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
