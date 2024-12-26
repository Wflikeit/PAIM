import pytest
from fastapi.testclient import TestClient
from infrastructure.api.main import app
from io import BytesIO
from unittest.mock import patch
from bson import ObjectId
import os

client = TestClient(app)


@pytest.mark.asyncio
async def test_upload_product():
    product_data = {
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025"
    }


    image_path = os.path.join(os.path.dirname(__file__), "test_images", "kartofel.jpeg")
    with open(image_path, "rb") as image_file:
        file_data = image_file.read()

    # (filename, content, mime_type)
    file = ("kartofel.jpeg", BytesIO(file_data), "image/jpeg")

    # Create product via upload API
    response = client.post(
        "http://localhost:8000/api/upload",
        data=product_data,
        files={"file": file}
    )
    
    assert response.status_code == 200
    assert "info" in response.json()
    assert "product_id" in response.json()

    product_id = response.json()["product_id"]

    return product_id


@pytest.mark.asyncio
async def test_get_product():
    id = await test_upload_product()

    mock_product_data = {
        "_id": id,
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025",
        "imageId": "675dbc6fcea393dd5e2c6f81"
    }

    with patch("infrastructure.product.product_repository.get_product_from_db", return_value=mock_product_data):
        response = client.get(f"http://localhost:8000/api/products/{id}")
        
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["product"]["name"] == mock_product_data["name"]
        assert float(data["product"]["price"]) == mock_product_data["price"]
        assert data["product"]["country_of_origin"] == mock_product_data["country_of_origin"]
        assert data["product"]["description"] == mock_product_data["description"]
        assert data["product"]["fruit_or_vegetable"] == mock_product_data["fruit_or_vegetable"]
        assert data["product"]["expiry_date"] == mock_product_data["expiry_date"]
    