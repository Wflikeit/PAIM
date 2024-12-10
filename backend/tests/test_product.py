import pytest
from fastapi.testclient import TestClient
from infrastructure.mongo.product_handler import get_product
from infrastructure.api.main import app
from io import BytesIO
from pymongo import MongoClient
from unittest.mock import patch
from bson import ObjectId


client = TestClient(app)


@pytest.mark.asyncio
async def test_upload_product():
    product_data = {
        "name": "Kartofelek",
        "price": 50.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "2025-12-31"
    }

    image_path = "tests/test_images/kartofel.jpeg"
    with open(image_path, "rb") as image_file:
        file_data = image_file.read()

    # (filename, content, mime_type)
    file = ("kartofel.jpeg", BytesIO(file_data), "image/jpeg")

    response = client.post(
        "http://localhost:8000/api/upload",
        data=product_data,
        files={"file": file}
    )
    
    assert response.status_code == 200
    assert "info" in response.json()
    assert "product_id" in response.json()


@pytest.mark.asyncio
async def test_get_product():
    product_data = {
        "name": "Kartofel",
        "price": 10.0,
        "country_of_origin": "Polska",
        "description": "Opis kartofla",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "01.12.2025",
    }

    client_mongo = MongoClient("mongodb://localhost:27017/")
    db = client_mongo["product"]
    
    product_id = ObjectId("67537e67b1e1ea00565c6e43")

    product_data = db["products"].find_one({"_id": product_id})
    assert product_data is not None, "Product not found in database"
    
    response = client.get(f"http://localhost:8000/api/products/{product_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["product"]["name"] == product_data["name"]
    assert data["product"]["price"] == product_data["price"]
    assert data["product"]["country_of_origin"] == product_data["country_of_origin"]
    assert data["product"]["description"] == product_data["description"]
    assert data["product"]["fruit_or_vegetable"] == product_data["fruit_or_vegetable"]
    assert data["product"]["expiry_date"] == product_data["expiry_date"]

@pytest.mark.asyncio
async def test_get_product_image():
    image_path = "tests/test_images/kartofel.jpeg"
    
    with open(image_path, "rb") as image_file:
        original_image_data = image_file.read()
        file_data = BytesIO(original_image_data)

    client_mongo = MongoClient("mongodb://localhost:27017/")
    db = client_mongo["product"]
    
    product_id = ObjectId("67537e67b1e1ea00565c6e43")

    image_id = db["products"].find_one({"_id": product_id})["imageId"]

    get_image_response = client.get(f"http://localhost:8000/api/images/{image_id}")

    assert get_image_response.status_code == 200, f"Response: {get_image_response.content}"

    returned_image_data = get_image_response.content
    assert returned_image_data == original_image_data, "The returned image does not match the uploaded image."
