from unittest.mock import AsyncMock
import pytest
from bson import ObjectId
from starlette.testclient import TestClient

from application.client.client_service import ClientService
from application.responses import ClientResponse
from domain.exceptions import ClientNotFoundError
from infrastructure.api.main import app
from infrastructure.containers import Container
from infrastructure.mongo.client_repository import ClientRepositoryMongo
from application.auth.auth import AuthService  # Import AuthService


@pytest.fixture(scope="module")
def test_container(mocked_client_repository):
    """Set up a test container with a test database."""
    container = Container()
    container.client_service.override(
        ClientService(client_repo=mocked_client_repository)
    )
    return container


@pytest.fixture(scope="module")
def test_client(test_container):
    """Fixture to create a test client with the container injected."""
    app.container = test_container
    return TestClient(app)


@pytest.fixture(scope="module")
def mocked_client_repository():
    """Fixture returning a mocked ClientRepositoryMongo."""
    return AsyncMock(ClientRepositoryMongo)


@pytest.fixture(scope="module")
def client_data():
    """Fixture returning data for a test client."""
    return {
        "email": "test@mail.com",
        "payment_address": "mock_payment_address",
        "delivery_address": "mock_delivery_address",
        "nip": "0123456789",
        "orders": "mock_orders",
        "password": "mock_password",
        "company_name": "mock_company_name",
    }


@pytest.fixture(scope="module")
def mock_client_data():
    """Fixture returning mock client data from the database."""
    return {
        "id": str(ObjectId()),
        "email": "test@mail.com",
        "payment_address": "mock_payment_address",
        "delivery_address": "mock_delivery_address",
        "nip": "0123456789",
        "orders": "mock_orders",
        "password": "mock_password",
        "company_name": "mock_company_name",
    }


@pytest.fixture(scope="module")
def mock_client_response(mock_client_data):
    """Fixture returning a mock client response."""
    return ClientResponse(**mock_client_data)


@pytest.fixture(scope="module")
def jwt_token():
    """Fixture to generate a test JWT token."""
    user_data = {"sub": "test@mail.com", "role": "admin"}
    return AuthService.create_access_token(data=user_data)


async def assert_client_response(mock_client_data, response_json):
    assert response_json["email"] == mock_client_data["email"]
    assert response_json["payment_address"] == mock_client_data["payment_address"]
    assert response_json["delivery_address"] == mock_client_data["delivery_address"]
    assert response_json["nip"] == mock_client_data["nip"]
    assert response_json["orders"] == mock_client_data["orders"]
    assert response_json["company_name"] == mock_client_data["company_name"]


@pytest.mark.asyncio
async def test_get_client_success(
        mock_client_data,
        mocked_client_repository,
        test_client,
        mock_client_response,
        jwt_token,
):
    """Test the integration of the /clients/{client_id} endpoint."""
    client_id = mock_client_data["id"]
    mocked_client_repository.get_client_db.return_value = mock_client_response

    response = test_client.get(
        f"/api/clients/{client_id}", headers={"Authorization": f"Bearer {jwt_token}"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == client_id
    await assert_client_response(mock_client_data, response_json)


@pytest.mark.asyncio
async def test_register_client_success(
        mocked_client_repository,
        test_client,
        client_data,
        mock_client_response,
        mock_client_data,
):
    """Test the integration of the /register endpoint."""
    mocked_client_repository.register_client_db.return_value = mock_client_response

    response = test_client.post(
        "/api/register",
        json=client_data,
    )

    assert response.status_code == 200
    response_json = response.json()
    await assert_client_response(mock_client_data, response_json)


@pytest.mark.asyncio
async def test_get_client_not_found(mocked_client_repository, test_client, jwt_token):
    """Test retrieving a client that does not exist."""
    non_existent_client_id = str(ObjectId())
    mocked_client_repository.get_client_db.side_effect = ClientNotFoundError(
        non_existent_client_id
    )

    response = test_client.get(
        f"/api/clients/{non_existent_client_id}",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )

    assert response.status_code == 404
    assert (
            response.json()["error"] == f"Client with ID {non_existent_client_id} not found"
    )


@pytest.mark.asyncio
async def test_get_client_invalid_id(
        mocked_client_repository, test_client, test_container, jwt_token
):
    """Test retrieving a client with invalid ID."""
    invalid_client_id = "not_a_valid_id"
    test_container.client_service.override(
        ClientService(client_repo=ClientRepositoryMongo())
    )

    response = test_client.get(
        f"/api/clients/{invalid_client_id}",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )

    assert response.status_code == 404
    assert (
            response.json()["error"]
            == f"ID: {invalid_client_id} is invalid: '{invalid_client_id}' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
    )
