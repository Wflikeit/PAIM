import abc
from typing import Optional

from application.requests import ProductResponse
from domain.product import Product


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    async def upload_product_to_db(
        self,
        product: Product,
    ) -> ProductResponse:
        pass

    # @abc.abstractmethod
    # def get_product_by_id(self, product_id: str) -> ProductResponse:
    #     pass

    # @abc.abstractmethod
    # def get_image_by_id(self, image_id: str) -> Optional[gridfs.GridOut]:
    #     pass
