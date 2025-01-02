from io import BytesIO
from unittest.mock import patch, AsyncMock

import pytest
from bson import ObjectId
from starlette.testclient import TestClient

from application.product.product_service import ProductService
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.product_repository import ProductRepositoryMongo


@pytest.fixture(scope="module")
def test_container():
    """Set up a test container with a test database."""
    container = Container()

    product_repository = ProductRepositoryMongo()
    container.product_service.override(ProductService(product_repo=product_repository))

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
        "imageId": "mocked_image_id",
    }


@pytest.fixture
def mocked_product_repository():
    """Fixture returning a mocked ProductRepositoryMongo."""
    return AsyncMock(ProductRepositoryMongo)


# 🎯 End-to-End Test
# This test covers the entire application flow
# ┌───────────┐   ┌──────────┐   ┌────────────┐   ┌───────────┐
# │   Client  │ → │   API    │ → │   Service  │ → │ Repository│
# └───────────┘   └──────────┘   └────────────┘   └───────────┘


@pytest.mark.asyncio
async def test_upload_product_success(test_client, product_data, test_container):
    """Test the full integration of the upload_product endpoint."""
    response = test_client.post(
        "/api/upload",
        data=product_data,
        files={"file": ("kartofel.jpeg", BytesIO(b"dummy image data"), "image/jpeg")},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert (
        response_json["info"]
        == f"Product '{product_data['name']}' uploaded successfully"
    )

    product_repository = test_container.product_service()._product_repo
    product = product_repository.get_product_by_id(response_json["product_id"])
    assert product["name"] == product_data["name"]
    assert product["price"] == product_data["price"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘


@pytest.mark.asyncio
async def test_get_product_not_found(test_client):
    """Test retrieving a product that does not exist."""
    non_existent_product_id = "non_existent_id"

    with patch(
        "infrastructure.mongo.product_repository.ProductRepositoryMongo.get_product_by_id",
        return_value=None,
    ):
        response = test_client.get(f"/api/products/{non_existent_product_id}")

        assert response.status_code == 404
        assert (
            response.json()["error"]
            == f"Product with ID {non_existent_product_id} not found"
        )


# @pytest.mark.asyncio
# async def test_get_product_image_not_found(test_client, mock_product_data, mocked_product_repository):
#     """Test retrieving an image for a product with no image."""
#     product_id = mock_product_data["_id"]
#
#     mocked_product_repository.get_product_by_id.return_value = mock_product_data
#
#     mocked_product_repository.get_image_by_id.return_value = None
#
#     response = test_client.get(f"/api/products/{product_id}/image")
#
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"Image for product {product_id} not found"


# 🧩 Unit Test
# This test focuses on a single service or function
# ┌────────────┐
# │   Service  │
# └────────────┘
@pytest.mark.asyncio
async def test_get_image_invalid_id(test_client):
    """Test retrieving an image with an invalid ID."""
    invalid_product_id = ObjectId(b"qwertyuiopas")

    response = test_client.get(f"/api/products/{invalid_product_id}/image")

    assert response.status_code == 404
    assert response.json()["error"] == f"Product with ID {invalid_product_id} not found"
