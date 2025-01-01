import base64
from typing import List
from bson import ObjectId

from application.product.product_repository import AbstractProductRepository
from application.responses import ProductResponse
from domain.exceptions import ProductNotFoundError
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
        product = self.product_collection.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise ProductNotFoundError(product_id)

        product["id"] = str(product["_id"])
        product["file"] = (
            f"data:image/jpeg;base64,{base64.b64encode(product["file"]).decode('utf-8')}"
        )

        return ProductResponse(**product)

    def get_all_products(self) -> List[ProductResponse]:
        products = list(self.product_collection.find())

        response_list = []
        for product in products:
            product["id"] = str(product["_id"])
            product["file"] = (
                f"data:image/jpeg;base64,{base64.b64encode(product["file"]).decode('utf-8')}"
            )
            response_list.append(ProductResponse(**product))

        return response_list
