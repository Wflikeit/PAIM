import abc
from typing import Optional
import gridfs

from domain.product import Product


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def upload_product_to_db(
        self,
        name: str,
        price: float,
        country_of_origin: str,
        description: str,
        fruit_or_vegetable: str,
        expiry_date: str,
        image_data: bytes,
    ) -> str:
        pass

    @abc.abstractmethod
    def get_product_by_id(self, product_id: str) -> Product:
        pass

    @abc.abstractmethod
    def get_image_by_id(self, image_id: str) -> Optional[gridfs.GridOut]:
        pass
