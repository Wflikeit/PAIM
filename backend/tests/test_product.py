import base64
from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from bson import ObjectId
from starlette.testclient import TestClient

from application.product.product_service import ProductService
from application.responses import ProductResponse
from domain.exceptions import EntityNotFoundError
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.product_repository import ProductRepositoryMongo


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
def mocked_product_repository():
    """Fixture returning a mocked ProductRepositoryMongo."""
    return AsyncMock(ProductRepositoryMongo)


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
    with open("test_images/kartofel.jpeg", "rb") as file:
        return file.read()


@pytest.fixture(scope="module")
def mocked_product_data(binary_file_data):
    """Fixture returning mock product data from the database."""
    base64_file_data = base64.b64encode(binary_file_data).decode("utf-8")

    return {
        "id": str(ObjectId()),
        "name": "Kartofelek",
        "price": 100.0,
        "country_of_origin": "Poland",
        "description": "Ziemniaczek",
        "fruit_or_vegetable": "Warzywo",
        "expiry_date": "10.12.2025",
        "file": f"data:image/jpeg;base64,{base64_file_data}",
    }


async def assert_product_response(mocked_product_data, response_json):
    assert response_json["name"] == mocked_product_data["name"]
    assert response_json["price"] == mocked_product_data["price"]
    assert (
        response_json["country_of_origin"] == mocked_product_data["country_of_origin"]
    )
    assert response_json["description"] == mocked_product_data["description"]
    assert (
        response_json["fruit_or_vegetable"] == mocked_product_data["fruit_or_vegetable"]
    )
    assert response_json["expiry_date"] == mocked_product_data["expiry_date"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_get_product_successful(
    mocked_product_data, binary_file_data, mocked_product_repository, test_client
):
    """Test the integration of the /products/{product_id} endpoint."""
    product_id = mocked_product_data["id"]
    mocked_product_response = ProductResponse(**mocked_product_data)
    mocked_product_repository.get_product_by_id.return_value = mocked_product_response

    response = test_client.get(f"/api/products/{product_id}")

    assert response.status_code == 200
    product = response.json()["products"]
    await assert_product_response(mocked_product_data, product)
    assert product["file"] == mocked_product_data["file"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_upload_product_success(
    mocked_product_data,
    binary_file_data,
    mocked_product_repository,
    test_client,
    product_data,
):
    """Test the full integration of the /upload endpoint."""
    mocked_product_response_data = ProductResponse(**mocked_product_data)
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
    await assert_product_response(product_data, response_json)
    assert response_json["file"] == mocked_product_data["file"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
def test_get_product_not_found(mocked_product_repository, test_client):
    """Test retrieving a product that does not exist."""
    non_existent_product_id = str(ObjectId())

    mocked_product_repository.get_product_by_id.side_effect = EntityNotFoundError("Product", non_existent_product_id)

    response = test_client.get(f"/api/products/{non_existent_product_id}")

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == f"Product with ID {non_existent_product_id} not found"
    )


@pytest.mark.asyncio
async def test_get_product_success(
    mocked_product_data,
    binary_file_data,
    mocked_product_repository,
    test_client,
    product_data,
    test_container,
):
    """End-to-end test of the /products/{product_id} endpoint."""
    product_id = "6775934ed79a82364c118356"
    test_container.product_service.override(
        ProductService(product_repo=ProductRepositoryMongo())
    )

    response = test_client.get(f"/api/products/{product_id}")

    assert response.status_code == 200
    product = response.json()["products"]
    await assert_product_response(product_data, product)
    assert product["file"] == mocked_product_data["file"]


@pytest.mark.asyncio
async def test_get_all_products_success(
    mocked_product_data,
    mocked_product_repository,
    test_client,
    product_data,
    test_container,
):
    """End-to-end test of the /products endpoint."""
    mocked_product_data["id"] = "6775934ed79a82364c118356"
    test_container.product_service.override(
        ProductService(product_repo=ProductRepositoryMongo())
    )

    response = test_client.get("/api/products")

    assert response.status_code == 200
    response_json = response.json()
    assert mocked_product_data in response_json["products"]


@pytest.mark.asyncio
async def test_upload_product_end_to_end(
    test_container, test_client, product_data, mocked_product_repository
):
    """End-to-end test of the /upload endpoint."""
    test_container.product_service.override(
        ProductService(product_repo=ProductRepositoryMongo())
    )
    with open("test_images/kartofel.jpeg", "rb") as image_file:
        response = test_client.post(
            "/api/upload",
            data=product_data,
            files={"file": ("xxx.jpeg", image_file, "image/jpeg")},
        )

    assert response.status_code == 200
    response_json = response.json()

    response_get = test_client.get(f"/api/products/{response_json['id']}")
    assert response_get.status_code == 200
    product = response_get.json()["products"]

    await assert_product_response(product, response_json)
    assert response_json["file"] == product["file"]


@pytest.mark.asyncio
async def test_get_product_invalid_id(test_client, test_container):
    """Test retrieving a client with invalid ID."""
    invalid_product_id = "not_a_valid_id"
    test_container.product_service.override(
        ProductService(product_repo=ProductRepositoryMongo())
    )

    response = test_client.get(f"/api/products/{invalid_product_id}")

    assert response.status_code == 404
    assert (
        response.json()["error"]
        == f"ID: {invalid_product_id} is invalid: '{invalid_product_id}' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
    )
