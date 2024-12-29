from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from starlette.responses import StreamingResponse
from starlette.testclient import TestClient

from application.product.product_service import ProductService
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.product_repository import ProductRepositoryMongo


@pytest.fixture(scope="module")
def test_container(mocked_product_repository):
    """Set up a test container with a test database."""
    container = Container()

    container.product_service.override(ProductService(product_repo=mocked_product_repository))

    return container


@pytest.fixture(scope="module")
def test_client(test_container):
    """Fixture to create a test client with the container injected."""
    app.container = test_container
    return TestClient(app)


@pytest.fixture(scope="module")
def product_data():
    """Fixture returning data for a test product."""
    return {
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025",
    }


@pytest.fixture(scope="module")
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
        "imageId": "mocked_image_id",
    }


@pytest.fixture(scope="module")
def mock_image_data():
    image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x8b\xc3'
    image_stream = BytesIO(image_data)
    filename = "mock_file_name.png"
    return StreamingResponse(
        image_stream,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@pytest.fixture(scope="module")
def mocked_product_repository():
    """Fixture returning a mocked ProductRepositoryMongo."""
    return AsyncMock(ProductRepositoryMongo)


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_upload_product_success(test_client, product_data, mocked_product_repository, mock_product_data):
    """Test the full integration of the /upload endpoint."""
    mocked_product_repository.upload_product_to_db.return_value = mock_product_data["_id"]
    response = test_client.post(
        "/api/upload",
        data=product_data,
        files={"file": ("kartofel.jpeg", BytesIO(b"dummy image data"), "image/jpeg")},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["info"] == f"Product '{product_data['name']}' uploaded successfully"


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_get_product_successful(test_client, mock_product_data, mocked_product_repository):
    """Test the integration of the /products/{product_id} endpoint."""
    product_id = mock_product_data["_id"]

    mocked_product_repository.get_product_by_id.return_value = mock_product_data
    response = test_client.get(f"/api/products/{product_id}")
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


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘

def test_get_product_not_found(test_client, mocked_product_repository):
    """Test retrieving a product that does not exist."""
    non_existent_product_id = "non_existent_id"

    mocked_product_repository.get_product_by_id.return_value = None
    response = test_client.get(f"/api/products/{non_existent_product_id}")

    assert response.status_code == 404
    assert response.json()["error"] == f"Product with ID {non_existent_product_id} not found"


