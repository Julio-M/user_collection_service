# in-built
from unittest import TestCase

# custom
from main import app

# 3rd party
from fastapi.testclient import TestClient

# in-built
from unittest import TestCase
from urllib.parse import urlencode, quote_plus

class TestAuthenticationEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
    
    def test_login_endpoint_with_valid_credentials(self):
        url = "/api/v1/login"
        payload = {'username': 'john2', 'password': 'password123'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        expected_keys = {'access_token','refresh_token', 'token_type'}

        response=self.client.post(
            url=url,
            headers=headers,
            data=urlencode(payload, quote_via=quote_plus)
        )

        response_data=response.json()

        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response_data)
        self.assertEqual(set(response_data),expected_keys)
    
    def test_login_endpoint_with_invalid_username(self):
        url = "/api/v1/login"
        payload = {'username': 'wrong', 'password': 'password123'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        expected_keys = {'detail'}

        response=self.client.post(
            url=url,
            headers=headers,
            data=urlencode(payload, quote_via=quote_plus)
        )

        response_data=response.json()

        self.assertIsNotNone(response_data)
        self.assertEqual(set(response_data),expected_keys)
        self.assertEqual(response.status_code, 401)


