from application.product.product_repository import AbstractProductRepository
from application.requests import ProductResponse
from domain.exceptions import ProductNotFoundError
from domain.product import Product


class ProductService:
    def __init__(self, product_repo: AbstractProductRepository) -> None:
        self._product_repo = product_repo

    async def upload_product(self, product_data: Product) -> ProductResponse:
        return await self._product_repo.upload_product_to_db(product=product_data)

    def get_product(self, product_id: str) -> ProductResponse:
        product_response = self._product_repo.get_product_by_id(product_id)
        if not product_response:
            raise ProductNotFoundError(product_id)
        return product_response
