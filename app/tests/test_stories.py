from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models.story import Story


def test_create_story():
    # Create a separate in-memory database for testing
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)

    # Override the dependency to use the test database
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    # Test with the client
    client = TestClient(app)
    
    # Test the regular story creation
    response = client.post(
        "/stories",
        json={"title": "Test Story", "description": "Test Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Story"
    assert data["description"] == "Test Description"
    assert "id" in data
    
    # Test the "New story" feature endpoint
    response = client.post(
        "/stories/new?title=New%20Story&description=New%20Description"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Story"
    assert data["description"] == "New Description"
    assert "id" in data

    # Clean up
    app.dependency_overrides.clear()