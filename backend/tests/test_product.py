import pytest
from fastapi.testclient import TestClient
from infrastructure.api.main import app
from io import BytesIO
from unittest.mock import patch
import os


@pytest.fixture
def client():
    """Fixture creating a test client for FastAPI."""
    return TestClient(app)


@pytest.fixture
def test_image_path():
    """Fixture returning the path to the test image file."""
    return os.path.join(os.path.dirname(__file__), "test_images", "kartofel.jpeg")


@pytest.fixture
def product_data():
    """Fixture returning data for a test product."""
    return {
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025"
    }


@pytest.fixture
def mock_product_data():
    """Fixture returning mock product data from the database."""
    return {
        "_id": "mocked_id",
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025",
        "imageId": "mocked_image_id"
    }


@pytest.mark.asyncio
async def test_upload_product(client, test_image_path, product_data):
    """Test uploading a product with an image."""
    with open(test_image_path, "rb") as image_file:
        file_data = image_file.read()

    file = ("kartofel.jpeg", BytesIO(file_data), "image/jpeg")

    response = client.post(
        "/api/upload",
        data=product_data,
        files={"file": file}
    )

    assert response.status_code == 200
    response_json = response.json()

    assert "info" in response_json
    assert "product_id" in response_json
    assert response_json["info"] == "Product 'Kartofelek' uploaded successfully"

    return response_json["product_id"]


@pytest.mark.asyncio
async def test_get_product(client, mock_product_data):
    """Test retrieving product details."""
    product_id = mock_product_data["_id"]

    # Mock the product repository
    with patch("infrastructure.product.product_repository.get_product_from_db", return_value=mock_product_data):
        response = client.get(f"/api/products/{product_id}")

        assert response.status_code == 200

        data = response.json()

        assert "product" in data
        product = data["product"]
        assert product["name"] == mock_product_data["name"]
        assert float(product["price"]) == mock_product_data["price"]
        assert product["country_of_origin"] == mock_product_data["country_of_origin"]
        assert product["description"] == mock_product_data["description"]
        assert product["fruit_or_vegetable"] == mock_product_data["fruit_or_vegetable"]
        assert product["expiry_date"] == mock_product_data["expiry_date"]
