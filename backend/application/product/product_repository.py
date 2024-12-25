import abc
from typing import Optional
import gridfs


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
    def get_product_from_db(self, product_id: str) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def get_image_from_db(self, image_id: str) -> Optional[gridfs.GridOut]:
        pass
