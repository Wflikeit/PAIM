import gridfs
from pymongo import MongoClient
from bson import ObjectId
from domain.product.model import Product
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_user = os.getenv("MONGO_USER")
client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@paim.yxyyk.mongodb.net/")
db = client["product"]
fs = gridfs.GridFS(db)

def upload_product_to_db(
    name: str,
    price: float,
    country_of_origin: str,
    description: str,
    fruit_or_vegetable: str,
    expiry_date: str,
    image_data: bytes,
) -> str:
    file_id = fs.put(image_data)

    product_data = {
        "name": name,
        "price": price,
        "country_of_origin": country_of_origin,
        "description": description,
        "fruit_or_vegetable": fruit_or_vegetable,
        "imageId": str(file_id),
        "expiry_date": expiry_date
    }

    product_collection = db["products"]
    product_id = product_collection.insert_one(product_data).inserted_id

    return str(product_id)

def get_product_from_db(product_id: str) -> Optional[dict]:
    product_collection = db["products"]
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    return product


def get_image_from_db(image_id: str) -> Optional[gridfs.GridOut]:
    try:
        image_id = ObjectId(image_id)
        return fs.get(image_id)
    except Exception:
        return None
