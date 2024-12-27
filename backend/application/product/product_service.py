from typing import Optional

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from application.product.product_repository import AbstractProductRepository
from domain.exceptions import ProductImageNotFoundError, ProductNotFoundError
from domain.product import Product


class ProductService:
    def __init__(self, product_repo: AbstractProductRepository) -> None:
        self._product_repo = product_repo

    async def upload_product(self, product_data: Product) -> dict:

        if not product_data:
            raise HTTPException(status_code=400, detail="Product data is missing")

        image_data = await product_data.file.read()

        if not image_data:
            raise HTTPException(
                status_code=400, detail="Image data is invalid or empty"
            )

        product_id = self._product_repo.upload_product_to_db(
            name=product_data.name,
            price=product_data.price,
            country_of_origin=product_data.country_of_origin,
            description=product_data.description,
            fruit_or_vegetable=product_data.fruit_or_vegetable,
            expiry_date=product_data.expiry_date,
            image_data=image_data,
        )

        return {
            "info": f"Product '{product_data.name}' uploaded successfully",
            "product_id": product_id,
        }

    def get_product(self, product_id: str):
        product = self._product_repo.get_product_by_id(product_id)

        if not product:
            raise ProductNotFoundError(product_id)

        product_info = {
            "name": product["name"],
            "price": product["price"],
            "country_of_origin": product["country_of_origin"],
            "description": product["description"],
            "fruit_or_vegetable": product["fruit_or_vegetable"],
            "expiry_date": product["expiry_date"],
            "imageId": product["imageId"],
        }

        return {"product": product_info}

    def get_image(self, product_id: str) -> Optional[StreamingResponse]:
        product = self._product_repo.get_product_by_id(product_id)

        if not product:
            raise ProductNotFoundError(product_id)

        image_response = self.fetch_image_for_product(product, product_id)
        return image_response

    def fetch_image_for_product(
        self, product: Product, product_id
    ) -> StreamingResponse:

        image_data = self._product_repo.get_image_by_id(product["imageId"])
        if not image_data:
            raise ProductImageNotFoundError(product_id)

        return StreamingResponse(
            image_data,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"attachment; filename={image_data.filename}"
            },
        )
