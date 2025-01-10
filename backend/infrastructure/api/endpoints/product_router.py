from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from application.auth.auth import AuthService
from application.product.product_service import ProductService
from application.responses import ProductResponse
from domain.product import Product
from infrastructure.containers import Container

router = APIRouter()


@router.post("/upload")
@inject
async def upload_product_endpoint(
    request: Request,
    product_service: ProductService = Depends(Provide[Container.product_service]),
    credentials: HTTPAuthorizationCredentials = Security(AuthService.security),
) -> ProductResponse:
    AuthService.is_admin(credentials=credentials)
    data = await request.form()
    file = data["file"]

    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPEG files are allowed")

    product = Product(**data)
    return await product_service.upload_product(product)


@router.get("/products/{product_id}", response_model=dict)
@inject
async def get_product(
    product_id: str,
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> dict:
    return {"product": product_service.get_product(product_id)}


@router.get("/products", response_model=dict)
@inject
async def get_products(
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> dict:
    return {"products": product_service.get_all_products()}
