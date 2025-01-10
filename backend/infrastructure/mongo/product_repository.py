import base64
import datetime
from typing import List

from bson import ObjectId

from application.product.product_repository import AbstractProductRepository
from application.responses import ProductResponse
from domain.entities import Entity
from domain.exceptions import EntityNotFoundError, InvalidIdError, InvalidDateType
from domain.product import Product
from infrastructure.mongo.mongo_client import MongoDBClient


class ProductRepositoryMongo(AbstractProductRepository):

    def __init__(self):
        self.product_collection = MongoDBClient.get_collection("products")

    async def upload_product_to_db(self, product: Product) -> ProductResponse:
        image_data = await product.file.read()

        product_data = product.model_dump()
        product_data["file"] = image_data
        result = self.product_collection.insert_one(product_data)
        product_data["id"] = str(result.inserted_id)
        product_data["file"] = (
            f"data:image/jpeg;base64,{base64.b64encode(product_data["file"]).decode('utf-8')}"
        )
        return ProductResponse(**product_data)

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        try:
            object_id = ObjectId(product_id)
        except Exception as err:
            raise InvalidIdError(Entity.product.value, str(err))
        product = self.product_collection.find_one({"_id": object_id})

        if not product:
            raise EntityNotFoundError(Entity.product.value, product_id)

        product["id"] = str(product["_id"])
        product["file"] = (
            f"data:image/jpeg;base64,{base64.b64encode(product["file"]).decode('utf-8')}"
        )

        product["expiry_date"] = product["expiry_date"].strftime("%Y-%m-%d")

        return ProductResponse(**product)

    def get_all_products(self) -> List[ProductResponse]:
        products = list(self.product_collection.find())

        response_list = []
        for product in products:
            product["id"] = str(product["_id"])
            product["file"] = (
                f"data:image/jpeg;base64,{base64.b64encode(product["file"]).decode('utf-8')}"
            )

            
            product["expiry_date"] = product["expiry_date"].strftime("%Y-%m-%d")
            response_list.append(ProductResponse(**product))

        return response_list
