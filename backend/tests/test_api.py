import unittest
from fastapi.testclient import TestClient
from src.api.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_app_exists(self):
        self.assertIsNotNone(app)

if __name__ == "__main__":
    unittest.main()