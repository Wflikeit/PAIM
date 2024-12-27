from io import BytesIO
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from infrastructure.api.main import app
from infrastructure.containers import Container
from application.product.product_service import ProductService
from infrastructure.mongo.product_repository import ProductRepositoryMongo


@pytest.fixture(scope="module")
def test_container():
    """Set up a test container with a test database."""
    container = Container()

    product_repository = ProductRepositoryMongo()
    container.product_service.override(
        ProductService(product_repo=product_repository)
    )

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
        "expiry_date": "10.12.2025"
    }


@pytest.mark.asyncio
async def test_upload_product_success(test_client, product_data, test_container):
    """Test the full integration of the upload_product endpoint."""
    response = test_client.post(
        "/api/upload",
        data=product_data,
        files={"file": ("kartofel.jpeg", BytesIO(b"dummy image data"), "image/jpeg")}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["info"] == f"Product '{product_data['name']}' uploaded successfully"

    product_repository = test_container.product_service()._product_repo
    product = product_repository.get_product_by_id(response_json["product_id"])
    assert product["name"] == product_data["name"]
    assert product["price"] == product_data["price"]

@pytest.mark.asyncio
async def test_get_product_not_found(test_client):
    """Test retrieving a product that does not exist."""
    non_existent_product_id = "non_existent_id"

    with patch("infrastructure.mongo.product_repository.ProductRepositoryMongo.get_product_by_id", return_value=None):
        response = test_client.get(f"/api/products/{non_existent_product_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == f"Product with ID {non_existent_product_id} not found"


# @pytest.mark.asyncio
# async def test_get_product_invalid_id(client):
#     """Test retrieving a product with an invalid ID."""
#     invalid_product_id = ObjectId("invalid_id")
#
#     response = client.get(f"/api/products/{invalid_product_id}")
#
#     assert response.status_code == 422
