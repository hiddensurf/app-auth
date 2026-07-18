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
def user_data_factory():
        def user_data():
            return {"full_name":fake.name(),
                    "user_name":fake.user_name(),
                    "email":fake.email(),
                    "password":fake.password(length=16)}
        return user_data
@pytest.fixture
def fake_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
@pytest.fixture
def registered_user(client,user_data_factory):
    user=user_data_factory()
    client.post("/signup",json=user)
    return user
    
