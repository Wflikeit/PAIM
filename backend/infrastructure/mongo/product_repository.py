import gridfs
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from typing import Optional

from application.product.product_repository import AbstractProductRepository
from infrastructure.mongo.mongo_client import MongoDBClient


class ProductRepositoryMongo(AbstractProductRepository):

    def __init__(self):
        self.db = MongoDBClient.get_database("product")
        self.fs = gridfs.GridFS(self.db)

    def upload_product_to_db(self,
        name: str,
        price: float,
        country_of_origin: str,
        description: str,
        fruit_or_vegetable: str,
        expiry_date: str,
        image_data: bytes,
    ) -> str:
        file_id = self.fs.put(image_data)

        product_data = {
            "name": name,
            "price": price,
            "country_of_origin": country_of_origin,
            "description": description,
            "fruit_or_vegetable": fruit_or_vegetable,
            "imageId": str(file_id),
            "expiry_date": expiry_date
        }

        product_collection = self.db["products"]
        product_id = product_collection.insert_one(product_data).inserted_id

        return str(product_id)

    def get_product_by_id(self, product_id: str) -> Optional[dict]:
        product_collection = self.db["products"]
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        return product


    def get_image_by_id(self, image_id: str) -> Optional[gridfs.GridOut]:
        return self.fs.get(ObjectId(image_id))

