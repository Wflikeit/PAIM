from typing import List

from application.product.product_repository import AbstractProductRepository
from application.responses import ProductResponse
from domain.product import Product


class ProductService:
    def __init__(self, product_repo: AbstractProductRepository) -> None:
        self._product_repo = product_repo

    async def upload_product(self, product_data: Product) -> ProductResponse:
        return await self._product_repo.upload_product_to_db(product=product_data)

    def get_product(self, product_id: str) -> ProductResponse:
        return self._product_repo.get_product_by_id(product_id)

    def get_all_products(self) -> List[ProductResponse]:
        return self._product_repo.get_all_products()
