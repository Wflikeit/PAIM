import base64
from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from bson import ObjectId
from starlette.testclient import TestClient

from application.product.product_service import ProductService
from application.requests import ProductResponse
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.product_repository import ProductRepositoryMongo


# TODO: rewrite pytest.fixtures to global variables so it runs faster
@pytest.fixture(scope="module")
def test_container(mocked_product_repository):
    """Set up a test container with a test database."""
    container = Container()

    container.product_service.override(
        ProductService(product_repo=mocked_product_repository)
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
        "expiry_date": "10.12.2025",
    }


@pytest.fixture(scope="module")
def binary_file_data():
    """Fixture returning sample binary data."""
    return b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00"


@pytest.fixture(scope="module")
def mocked_product_data(binary_file_data):
    """Fixture returning mock product data from the database."""
    base64_file_data = base64.b64encode(binary_file_data).decode(
        "utf-8"
    )  # Convert to Base64

    return {
        "id": str(ObjectId()),
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025",
        "file": base64_file_data,
    }


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
async def test_get_product_successful(
    test_client, mocked_product_data, mocked_product_repository
):
    """Test the integration of the /products/{product_id} endpoint."""
    product_id = ObjectId(mocked_product_data["id"])
    mocked_product_repository.get_product_by_id.return_value = ProductResponse(
        **mocked_product_data
    )

    response = test_client.get(f"/api/products/{product_id}")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == mocked_product_data["name"]
    assert float(response_json["price"]) == mocked_product_data["price"]
    assert (
        response_json["country_of_origin"] == mocked_product_data["country_of_origin"]
    )
    assert response_json["description"] == mocked_product_data["description"]
    assert (
        response_json["fruit_or_vegetable"] == mocked_product_data["fruit_or_vegetable"]
    )
    assert response_json["expiry_date"] == mocked_product_data["expiry_date"]
    assert response_json["file"] == mocked_product_data["file"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_upload_product_success(
    test_container,
    test_client,
    product_data,
    mocked_product_repository,
    mocked_product_data,
    binary_file_data,
):
    """Test the full integration of the /upload endpoint."""

    # Uncomment to use real MongoDB
    # test_container.product_service.override(
    #     ProductService(product_repo=ProductRepositoryMongo())
    # )
    mocked_product_response_data = ProductResponse(**mocked_product_data)
    mocked_product_response_data.file = str(binary_file_data)
    mocked_product_repository.upload_product_to_db.return_value = (
        mocked_product_response_data
    )

    base64_file_data = mocked_product_data["file"]
    file_data = BytesIO(base64.b64decode(base64_file_data))

    response = test_client.post(
        "/api/upload",
        data=product_data,
        files={"file": ("xxx.jpeg", file_data, "image/jpeg")},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == product_data["name"]
    assert response_json["price"] == product_data["price"]
    assert response_json["country_of_origin"] == product_data["country_of_origin"]
    assert response_json["description"] == product_data["description"]
    assert response_json["fruit_or_vegetable"] == product_data["fruit_or_vegetable"]
    assert response_json["expiry_date"] == product_data["expiry_date"]
    response_file_base64 = base64.b64encode(eval(response_json["file"])).decode("utf-8")
    assert response_file_base64 == base64_file_data


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
def test_get_product_not_found(test_client, mocked_product_repository, test_container):
    """Test retrieving a product that does not exist."""
    non_existent_product_id = str(ObjectId())
    # currently works only with MongoDB
    # TODO: fix rasing ProductNotFoundError with mocked repository
    test_container.product_service.override(
        ProductService(product_repo=ProductRepositoryMongo())
    )

    response = test_client.get(f"/api/products/{non_existent_product_id}")

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == f"Product with ID {non_existent_product_id} not found"
    )
