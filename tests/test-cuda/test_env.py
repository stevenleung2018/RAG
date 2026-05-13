# test_env.py

# This script is for testing by GitHub CI to make sure that the env_cuda.yml file actually works

import torch
import sys
import importlib
import pytest
import os

def running_in_ci() -> bool:
    return os.getenv("CI") in ("true", "1") or os.getenv("GITHUB_ACTIONS") == "true"

@pytest.mark.skipif(running_in_ci(), reason="Skip runtime CUDA availability check on CI (no GPU/drivers)")
def test_pytorch_cuda_runtime_available():
    # This test requires a GPU + drivers; skip on CI
    assert torch.cuda.is_available(), "Expected CUDA runtime available (GPU + drivers)"

def test_pytorch_cuda_build_metadata():
    # Always run: checks build-time CUDA support (packages) without requiring hardware
    version = torch.__version__
    cuda_version = getattr(torch.version, "cuda", None)
    built_flag = False
    try:
        built_flag = torch.backends.cuda.is_built()
    except Exception:
        built_flag = False

    has_cu_suffix = "+cu" in version
    has_cuda_build = built_flag or (cuda_version is not None) or has_cu_suffix

    print(f"torch.__version__ = {version}")
    print(f"torch.version.cuda = {cuda_version!r}")
    print(f"torch.backends.cuda.is_built() = {built_flag}")
    assert has_cuda_build, (
        "PyTorch does not appear to be built with CUDA support. "
        f"torch.__version__={version}, torch.version.cuda={cuda_version}, "
        f"torch.backends.cuda.is_built()={built_flag}"
    )

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
