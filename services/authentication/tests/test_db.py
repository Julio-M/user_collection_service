# in-built
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base_class import Base
from api.deps import get_db

from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "http://0.0.0.0:9558/api/v1/signup/",
        json={
            "first_name": "john",
            "last_name": "doe",
            "email": "user2@example.com",
            "username": "johndoe2",
            "is_active": True,
            "password": "secret"
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["first_name"] == "john"
    assert data["last_name"] == "doe"
    assert data["username"] == "johndoe"
    assert "id" in data
