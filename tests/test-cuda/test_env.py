# test_env_cuda.py

# This script is for testing by GitHub CI to make sure that the env_cuda.yml file actually works

import torch
import sys
import importlib


def test_python_version():
    """Test that Python 3.12 or compatible version is installed"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 12
    print(f"✓ Python version: {sys.version}")


def test_pytorch_installation():
    """Test that PyTorch is installed and importable"""
    assert torch is not None
    assert hasattr(torch, "__version__")
    print(f"✓ PyTorch version: {torch.__version__}")
    print(f"✓ PyTorch location: {torch.__file__}")


def test_pytorch_cuda_support():
    """Test that PyTorch has CUDA support (available or
    compiled with CUDA)"""
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"✓ CUDA available: {cuda_available}")
    if cuda_available:
        print(f"  - CUDA device: {torch.cuda.get_device_name(0)}")
        print(f"  - CUDA device count: {torch.cuda.device_count()}")
    # The test passes if either CUDA is available or PyTorch
    # was compiled with CUDA support
    assert "cu" in torch.__version__ or cuda_available


def test_mps_availability():
    """Test that MPS availability can be checked
    (doesn't require it to be available)"""
    mps_available = torch.backends.mps.is_available()
    print(f"✓ MPS available: {mps_available}")


def test_required_packages():
    """Test that required packages are installed"""
    required_packages = [
        "transformers",
        "sentence_transformers",
        "langchain",
        "langchain_community",
        "pymupdf",
        "faiss",
        "accelerate",
        "bitsandbytes",
        "pandas",
        "numpy",
        "scipy",
        "sklearn",
        "ipykernel",
    ]
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} installed")
        except ImportError:
            raise AssertionError(f"Required package '{package}' not found")


def test_pytorch_basic_operations():
    """Test that basic PyTorch operations work"""
    # Create a simple tensor
    x = torch.randn(2, 3)
    assert x.shape == (2, 3)
    print("✓ Basic tensor creation works")
    
    # Test device detection
    if torch.cuda.is_available():
        device_type = "cuda"
    elif torch.backends.mps.is_available():
        device_type = "mps"
    else:
        device_type = "cpu"
    print(f"✓ Detected device type: {device_type}")


if __name__ == "__main__":
    print(f"Python executable: {sys.executable}\n")
    test_python_version()
    test_pytorch_installation()
    test_pytorch_cuda_support()
    test_mps_availability()
    test_required_packages()
    test_pytorch_basic_operations()
    print("\n✓ All tests passed!")
