from bson import ObjectId

from application.product.product_repository import AbstractProductRepository
from application.requests import ProductResponse
from domain.exceptions import ProductNotFoundError
from domain.product import Product
from infrastructure.mongo.mongo_client import MongoDBClient


class ProductRepositoryMongo(AbstractProductRepository):

    def __init__(self):
        self.db = MongoDBClient.get_database("product")

    async def upload_product_to_db(self, product: Product) -> ProductResponse:
        product_collection = self.db["products"]
        image_data = await product.file.read()

        product_data = product.model_dump()
        product_data["file"] = image_data
        result = product_collection.insert_one(product_data)
        product_data["file"] = str(image_data)
        product_data["id"] = str(result.inserted_id)
        return ProductResponse(**product_data)

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        product_collection = self.db["products"]
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise ProductNotFoundError(product_id)
        return ProductResponse(**product)
