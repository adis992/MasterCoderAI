#!/usr/bin/env python3
"""Test model direktno bez backend-a"""
from llama_cpp import Llama

print("🚀 Loading model direktno...")
model = Llama(
    model_path="/root/MasterCoderAI/modeli/DarkIdol-Lama3.1.gguf",
    n_ctx=8192,
    n_threads=4,
    n_gpu_layers=-1,
    verbose=False
)

print("✅ Model loaded!")
print("\n🤖 Testing simple prompt...")

response = model(
    "Say only 'Hello' and nothing else:",
    max_tokens=10,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1,
    echo=False
)

print(f"Response: {response['choices'][0]['text']}")
print(f"\nTokens: {response['usage']}")
