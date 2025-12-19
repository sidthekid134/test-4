from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from ..main import app
from ..database import get_session
from ..models.item import Item


# Create a test database in memory
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_item(client):
    response = client.post(
        "/api/items/",
        json={"name": "Test Item", "description": "This is a test item"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_items(client, session):
    # Create test items
    session.add(Item(name="Item 1", description="Description 1"))
    session.add(Item(name="Item 2", description="Description 2"))
    session.commit()

    response = client.get("/api/items/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"


def test_read_item(client, session):
    # Create a test item
    item = Item(name="Single Item", description="Test Description")
    session.add(item)
    session.commit()

    response = client.get(f"/api/items/{item.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Single Item"
    assert data["description"] == "Test Description"
    assert data["id"] == item.id


def test_update_item(client, session):
    # Create a test item
    item = Item(name="Update Item", description="Before Update")
    session.add(item)
    session.commit()

    response = client.patch(
        f"/api/items/{item.id}",
        json={"name": "Updated Name", "description": "After Update"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Updated Name"
    assert data["description"] == "After Update"


def test_delete_item(client, session):
    # Create a test item
    item = Item(name="Delete Item", description="Will be deleted")
    session.add(item)
    session.commit()

    response = client.delete(f"/api/items/{item.id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/items/{item.id}")
    assert response.status_code == 404