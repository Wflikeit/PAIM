import os
from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from application.order.order_service import OrderService
from application.responses import WarehouseResponse
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.client_repository import ClientRepositoryMongo
from infrastructure.mongo.order_repository import OrderRepositoryMongo
from infrastructure.mongo.truck_repository import TruckRepositoryMongo
from infrastructure.mongo.warehouse_repository import WarehouseRepositoryMongo

os.environ["MONGO_DATABASE"] = "shop_db_dev"


@pytest.fixture(scope="module")
def test_container(
        mocked_client_repository, mocked_warehouse_repository, mocked_order_repository, mocked_truck_repository
):
    """Set up a test container with a test database."""
    container = Container()
    container.order_service.override(
        OrderService(
            order_repo=mocked_order_repository,
            client_repo=mocked_client_repository,
            warehouse_repo=mocked_warehouse_repository,
            truck_repo=mocked_truck_repository
        )
    )
    return container


@pytest.fixture(scope="module")
def test_client(test_container):
    """Fixture to create a test client with the container injected."""
    app.container = test_container
    return TestClient(app)


@pytest.fixture(scope="module")
def mocked_client_repository():
    """Fixture returning a mocked OrderRepositoryMongo."""
    return AsyncMock(ClientRepositoryMongo)


@pytest.fixture(scope="module")
def mocked_order_repository():
    """Fixture returning a mocked OrderRepositoryMongo."""
    return AsyncMock(OrderRepositoryMongo)


@pytest.fixture(scope="module")
def mocked_warehouse_repository():
    """Fixture returning a mocked WarehouseRepositoryMongo."""
    return AsyncMock(WarehouseRepositoryMongo)


@pytest.fixture(scope="module")
def mocked_truck_repository():
    """Fixture returning a mocked TruckRepositoryMongo."""
    return AsyncMock(TruckRepositoryMongo)


@pytest.fixture(scope="module")
def order_data():
    """Fixture returning data for a test order."""
    return {
        "delivery_date": "11.05.2025",
        "amount": 600.5,
        "products": [
            {"product_id": "1", "quantity": 4.0},
            {"product_id": "2", "quantity": 5.0},
            {"product_id": "3", "quantity": 6.0},
            {"product_id": "4", "quantity": 7.0},
            {"product_id": "5", "quantity": 8.0},
        ],
        "delivery_address": "0123456789",
        "order_status": "pending",
        "email": "mocked@mail.com",
        "route_length": 123,
    }


@pytest.fixture(scope="module")
def mock_warehouse_data():
    """Fixture returning a mocked warehouse data."""
    return [
        {
            "id": "1",
            "address": "Warehouse Partial 1",
            "product_quantities": {"1": 6.0, "2": 5.0, "4": 8.0, "3": 1.5, "5": 1.5},
            "trucks": ["Truck-1", "Truck-4"],
        },
        {
            "id": "2",
            "address": "Warehouse Partial 2",
            "product_quantities": {"3": 7.0, "5": 9.0, "1": 1.5, "2": 1.5, "4": 1.5},
            "trucks": ["Truck-3", "Truck-5"],
        },
        {
            "id": "3",
            "address": "Warehouse Partial 3",
            "product_quantities": {"1": 7.0, "3": 8.0, "4": 9.0, "2": 1.5, "5": 1.5},
            "trucks": ["Truck-2"],
        },
        {
            "id": "4",
            "address": "Warehouse Partial 4",
            "product_quantities": {"2": 5.0, "4": 8.0, "1": 1.5, "3": 1.5, "5": 1.5},
            "trucks": ["Truck-1", "Truck-3"],
        },
        {
            "id": "5",
            "address": "Warehouse Partial 5",
            "product_quantities": {"1": 6.0, "2": 5.0, "5": 9.0, "3": 1.5, "4": 1.5},
            "trucks": ["Truck-4"],
        },
        {
            "id": "6",
            "address": "Warehouse Partial 6",
            "product_quantities": {"1": 8.0, "3": 9.0, "2": 1.5, "4": 1.5, "5": 1.5},
            "trucks": ["Truck-2", "Truck-5"],
        },
        {
            "id": "7",
            "address": "Warehouse Partial 7",
            "product_quantities": {"2": 6.0, "5": 9.0, "1": 1.5, "3": 1.5, "4": 1.5},
            "trucks": ["Truck-1", "Truck-4"],
        },
        {
            "id": "8",
            "address": "Warehouse Partial 8",
            "product_quantities": {"3": 7.0, "4": 9.0, "1": 1.5, "2": 1.5, "5": 1.5},
            "trucks": ["Truck-3"],
        },
        {
            "id": "9",
            "address": "Warehouse Full",
            "product_quantities": {"1": 5.0, "2": 4.0, "3": 6.0, "4": 7.0, "5": 8.0},
            "trucks": ["Truck-2", "Truck-4", "Truck-5"],
        },
        {
            "id": "10",
            "address": "Warehouse Partial 9",
            "product_quantities": {"1": 6.0, "2": 3.0, "5": 7.0, "3": 1.5, "4": 1.5},
            "trucks": ["Truck-1", "Truck-3"],
        },
    ]


@pytest.fixture(scope="module")
def mock_warehouse_response(mock_warehouse_data):
    """Fixture returning a mocked list of warehouse responses."""
    response = []
    for warehouse_item in mock_warehouse_data:
        response.append(WarehouseResponse(**warehouse_item))
    return response

@pytest.fixture(scope="module")
def mock_order_response():
    """Fixture returning a mocked order response."""
    return {
        "id": "677c3333e6ba26d342d1786d",
        "delivery_date": "11.05.2025",
        "amount": 600.5,
        "products": [{
            "product_id": "1",
            "quantity": 4.0
        },
            {
                "product_id": "2",
                "quantity": 5.0
            },
            {
                "product_id": "3",
                "quantity": 6.0
            },
            {
                "product_id": "4",
                "quantity": 7.0
            },
            {
                "product_id": "5",
                "quantity": 8.0
            }
        ],
        "delivery_address": "0123456789",
        "order_status": "pending",
        "email": "mocked@mail.com",
        "trucks": [
            "677b2e6e58135031873da9db"
        ],
        "warehouses": [
            "6779eba8536d018b5bbd8a50"
        ],
        "route_length": 123.0
    }

async def assert_order_response(mock_order_data, response_json):
    assert response_json["delivery_date"] == mock_order_data["delivery_date"]
    assert response_json["amount"] == mock_order_data["amount"]
    assert response_json["products"] == mock_order_data["products"]
    assert response_json["delivery_address"] == mock_order_data["delivery_address"]
    assert response_json["order_status"] == mock_order_data["order_status"]
    assert response_json["email"] == mock_order_data["email"]
    assert response_json["trucks"] == mock_order_data["trucks"]
    assert response_json["warehouses"] == mock_order_data["warehouses"]
    assert response_json["route_length"] == mock_order_data["route_length"]

@pytest.mark.asyncio
async def test_add_order_success_end_to_end(
        test_client,
        test_container,
        order_data,
        mock_order_response
):
    """End-to-end test the of the /purchase endpoint."""
    test_container.order_service.override(
        OrderService(
            order_repo=OrderRepositoryMongo(),
            client_repo=ClientRepositoryMongo(),
            warehouse_repo=WarehouseRepositoryMongo(),
            truck_repo=TruckRepositoryMongo()
        )
    )

    response = test_client.post("/api/purchase", json=order_data)

    assert response.status_code == 200
    response_json = response.json()
    await assert_order_response(mock_order_response, response_json)
