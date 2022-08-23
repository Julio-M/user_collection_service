# in-built
from unittest import TestCase

# custom
from ..main import app

# 3rd party
from fastapi.testclient import TestClient

client = TestClient(app)


def test_login():
    url = "http://0.0.0.0:9558/api/v1/login"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "hello from login endpoint"}
