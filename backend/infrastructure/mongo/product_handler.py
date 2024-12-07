import gridfs
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException

client = MongoClient("mongodb://localhost:27017/")
db = client["product"]
fs = gridfs.GridFS(db)

def upload_product(name: str, price: float, country_of_origin:str, description: str, fruit_or_vegetable:str, image_data: bytes, expiry_date: str, filename: str) -> str:
    file_id = fs.put(image_data, filename=filename)
    
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

def get_product(product_id: str) -> Optional[dict]:
    try:
        product_collection = db["products"]
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_image(id: str) -> Optional[gridfs.GridOut]:
    try:
        image_id = ObjectId(id)
        return fs.get(image_id)
    except gridfs.errors.NoFile:
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
