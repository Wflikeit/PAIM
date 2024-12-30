from unittest.mock import AsyncMock

import pytest
from bson import ObjectId
from starlette.testclient import TestClient

from application.client.client_service import ClientService
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.client_repository import ClientRepositoryMongo

container = Container()
mocked_client_repository = AsyncMock(ClientRepositoryMongo)
container.client_service.override(ClientService(client_repo=mocked_client_repository))
app.container = container
test_client = TestClient(app)

client_data = {
    "email": "test@mail.com",
    "payment_address": "mock_payment_address",
    "delivery_address": "mock_delivery_address",
    "nip": "0123456789",
    "orders": "mock_orders",
    "password": "mock_password",
    "company_name": "mock_company_name",
}

mock_client_data = {
    "_id": str(ObjectId()),
    "email": "test@mail.com",
    "payment_address": "mock_payment_address",
    "delivery_address": "mock_delivery_address",
    "nip": "0123456789",
    "orders": "mock_orders",
    "password": "mock_password",
    "company_name": "mock_company_name",
}


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_register_client_success():
    """Test the integration of the /register endpoint."""
    mocked_client_repository.register_client_db.return_value = mock_client_data["_id"]

    response = test_client.post("/api/register", data=client_data)

    assert response.status_code == 200
    response_json = response.json()
    assert (
        response_json["info"]
        == f"Client '{client_data["email"]}' registered successfully"
    )


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_get_client_success():
    """Test the integration of the /clients/{client_id} endpoint."""
    client_id = mock_client_data["_id"]
    mocked_client_repository.get_client_db.return_value = mock_client_data

    response = test_client.get(f"/api/clients/{client_id}")

    assert response.status_code == 200
    data = response.json()
    assert "client" in data
    client = data["client"]
    assert client["email"] == client_data["email"]
    assert client["payment_address"] == client_data["payment_address"]


# 🔗 Integration Test
# This test ensures API and service layers work together
# ┌───────────┐   ┌──────────┐   ┌────────────┐
# │   Client  │ → │   API    │ → │   Service  │
# └───────────┘   └──────────┘   └────────────┘
@pytest.mark.asyncio
async def test_get_product_not_found():
    """Test retrieving a client that does not exist."""
    non_existent_client_id = str(ObjectId())
    # currently works only with MongoDB
    # TODO: fix rasing ClientNotFoundError with mocked repository
    container.client_service.override(
        ClientService(client_repo=ClientRepositoryMongo())
    )

    response = test_client.get(f"/api/clients/{non_existent_client_id}")

    assert response.status_code == 404
    assert (
        response.json()["error"] == f"Client with ID {non_existent_client_id} not found"
    )
