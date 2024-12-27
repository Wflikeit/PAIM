import os
import threading
from dotenv import load_dotenv
from pymongo import MongoClient

class MongoDBClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    load_dotenv()
                    mongo_password = os.getenv("MONGO_PASSWORD")
                    mongo_user = os.getenv("MONGO_USER")
                    mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@paim.yxyyk.mongodb.net/"
                    cls._instance = MongoClient(mongo_uri)
        return cls._instance

    @staticmethod
    def get_database(db_name: str):
        return MongoDBClient().get_database(db_name)
