# AI Engine

The AI Engine module is responsible for loading and managing machine learning models. It includes components for hybrid models, prompt engineering, and model supervision.

## Features
- Model loading and initialization
- Hybrid model integration
- Prompt engineering utilities

## Usage
```python
from src.ai_engine.model_loader import ModelLoader

loader = ModelLoader("path/to/model")
model = loader.load_transformer_model("model_name")
```