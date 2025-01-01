from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from starlette.requests import Request

from application.product.product_service import ProductService
from application.responses import ProductResponse
from domain.product import Product
from infrastructure.containers import Container

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


@router.get("/products", response_model=dict)
@inject
async def get_products(
    id: Optional[str] = Query(None, description="Filter by product id"),
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> dict:
    if id:
        products = product_service.get_product(id)
    else:
        products = product_service.get_all_products()
    return {"products": products}
