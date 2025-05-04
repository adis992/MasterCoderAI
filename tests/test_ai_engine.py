# Boilerplate unit test for ai_engine
import unittest
from src.ai_engine.model_loader import ModelLoader

class TestAIEngine(unittest.TestCase):
    def test_model_loader(self):
        loader = ModelLoader("dummy_model_dir")
        self.assertIsNotNone(loader)

if __name__ == "__main__":
    unittest.main()