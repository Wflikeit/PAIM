import gridfs
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from domain.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_user = os.getenv("MONGO_USER")
client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@paim.yxyyk.mongodb.net/")
db = client["client"]
fs = gridfs.GridFS(db)

def register_client_db(client: Client) -> str:
    client_dict = client.dict()
    client_collection = db["clients"]
    client_id = client_collection.insert_one(client_dict).inserted_id
    
    return str(client_id)

def get_client_db(client_id: str) -> Optional[dict]:
    try:
        client_collection = db["clients"]
        client = client_collection.find_one({"_id": ObjectId(client_id)})
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
