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
                    load_dotenv()  # Load environment variables from .env file
                    mongo_user = os.getenv("MONGO_USER")
                    mongo_password = os.getenv("MONGO_PASSWORD")
                    mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@paim.yxyyk.mongodb.net/"
                    try:
                        cls._instance = MongoClient(
                            mongo_uri, serverSelectionTimeoutMS=5000
                        )
                        # Test connection
                        cls._instance.admin.command("ping")
                    except ConnectionError as e:
                        raise RuntimeError("Could not connect to MongoDB") from e
        return cls._instance

    @staticmethod
    def get_database():
        load_dotenv(override=False)
        mongo_database = os.getenv("MONGO_DATABASE")
        if not mongo_database:
            raise ValueError("MONGO_DATABASE is not set in .env file")
        return MongoDBClient()[mongo_database]

    @staticmethod
    def get_collection(collection_name: str):
        database = MongoDBClient.get_database()
        return database[collection_name]
