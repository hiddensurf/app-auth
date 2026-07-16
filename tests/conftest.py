import pytest
from app.main import app
from app.database.database import create_session
from tests.database import create_test_session
from fastapi.testclient import TestClient
from faker import Faker
fake = Faker()

@pytest.fixture
def client():
    app.dependency_overrides[create_session] = create_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
@pytest.fixture
def user_data():
    return {"full_name":fake.name(),
            "user_name":fake.user_name(),
            "email":fake.email(),
            "password":fake.password(length=16)}
    
