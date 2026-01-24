#!/usr/bin/env python3
"""
Test CUDA support in llama-cpp-python
"""

print("=" * 60)
print("🔍 Testing CUDA Support in llama-cpp-python")
print("=" * 60)

try:
    from llama_cpp import Llama
    print("✅ llama-cpp-python imported successfully")
except ImportError as e:
    print(f"❌ Failed to import llama-cpp-python: {e}")
    exit(1)

# Check version
try:
    import llama_cpp
    print(f"📦 Version: {llama_cpp.__version__}")
except:
    print("⚠️  Could not determine version")

# Try to check CUDA support
print("\n🔬 Checking CUDA support...")
try:
    # Try to access the underlying C library
    import llama_cpp.llama_cpp as llama_cpp_lib
    
    # Check if GPU functions exist
    if hasattr(llama_cpp_lib, 'llama_supports_gpu_offload'):
        print("✅ GPU offload functions found!")
        
        # Try to call it
        try:
            supports_gpu = llama_cpp_lib.llama_supports_gpu_offload()
            if supports_gpu:
                print("🎉 CUDA SUPPORT CONFIRMED!")
            else:
                print("⚠️  GPU offload functions exist but returned False")
        except Exception as e:
            print(f"⚠️  Could not call GPU function: {e}")
    else:
        print("❌ NO GPU offload functions found - CUDA NOT COMPILED")
        print("   This version is CPU-only")
        
except Exception as e:
    print(f"⚠️  Could not check CUDA support: {e}")

# Test creating a Llama instance with GPU
print("\n🧪 Testing GPU initialization...")
try:
    # Create minimal test - this will fail if no CUDA
    test_model = Llama(
        model_path="/root/MasterCoderAI/modeli/DarkIdol-Lama3.1.gguf",
        n_ctx=512,
        n_gpu_layers=1,  # Try to load just 1 layer to GPU
        verbose=True
    )
    print("🎉 SUCCESS! Model initialized with n_gpu_layers=1")
    print("   CUDA support is working!")
    del test_model
except Exception as e:
    print(f"❌ Failed to initialize with GPU: {e}")
    print("   This likely means CUDA is NOT compiled in")

print("\n" + "=" * 60)
