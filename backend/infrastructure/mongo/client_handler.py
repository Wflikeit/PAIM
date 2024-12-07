import gridfs
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException

client = MongoClient("mongodb://localhost:27017/")
db = client["client"]
fs = gridfs.GridFS(db)

def register_client(email: str, payment_address: str, delivery_address:str, nip: str, orders:str, password: str, company_name: str) -> str:

    client_data = {
        "email": email,
        "payment_address": payment_address,
        "delivery_address": delivery_address,
        "nip": nip,
        "orders": orders,
        "password": password,
        "company_name": company_name
    }
    
    client_collection = db["clients"]
    client_id = client_collection.insert_one(client_data).inserted_id
    
    return str(client_id)

def get_client(client_id: str) -> Optional[dict]:
    try:
        client_collection = db["clients"]
        client = client_collection.find_one({"_id": ObjectId(client_id)})
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
