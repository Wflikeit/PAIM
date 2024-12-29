from bson import Binary

from application.product.product_repository import AbstractProductRepository
from application.requests import ProductResponse
from domain.product import Product
from infrastructure.mongo.mongo_client import MongoDBClient


class ProductRepositoryMongo(AbstractProductRepository):

    def __init__(self):
        self.db = MongoDBClient.get_database("product")

    async def upload_product_to_db(self, product: Product) -> ProductResponse:
        product_collection = self.db["products"]
        image_data = await product.file.read()

        product_data = product.model_dump()
        product_data["file"] = Binary(image_data)
        result = product_collection.insert_one(product_data)

        product_data["id"] = str(result.inserted_id)
        return ProductResponse(**product_data)

    # def get_product_by_id(self, product_id: str) -> Optional[dict]:
    #     product_collection = self.db["products"]
    #     product = product_collection.find_one({"_id": ObjectId(product_id)})
    #     return product
    #
    # def get_image_by_id(self, image_id: str) -> Optional[gridfs.GridOut]:
    #     return self.fs.get(ObjectId(image_id))
