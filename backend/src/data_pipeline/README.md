# Data Pipeline

The Data Pipeline module handles data validation, augmentation, and vector database management. It ensures data integrity and prepares data for machine learning workflows.

## Features

- Data validation
- Data augmentation
- Vector database management

## Usage

```python
from src.data_pipeline.data_validator import DataValidator
from src.data_pipeline.data_augmenter import DataAugmenter
from src.data_pipeline.vector_db import VectorDB

validator = DataValidator()
if validator.validate(data):
    print("Data is valid!")

data = ...
augmented = DataAugmenter().augment(data)

db = VectorDB()
db.insert_vector(augmented)
```