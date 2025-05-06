# Boilerplate unit test for data_pipeline
import unittest
from src.data_pipeline.data_validator import DataValidator

class TestDataPipeline(unittest.TestCase):
    def test_validator(self):
        validator = DataValidator()
        self.assertTrue(validator.validate_json({"field": "value"}, ["field"]))

if __name__ == "__main__":
    unittest.main()