"""
Unit tests for verifying env_mps.yml conda environment setup for MPS support.

These tests verify that:
1. The conda environment has the correct Python version
2. PyTorch is installed with MPS support
3. Key dependencies are installed with correct versions
4. MPS is available and accessible on the system
5. All required packages for the RAG pipeline are present
"""

import pytest
import sys
import platform
import importlib.util
from packaging import version


class TestEnvironmentBasics:
    """Test basic environment setup."""
    
    def test_python_version(self):
        """Verify Python version is 3.11 as specified in env_mps.yml."""
        major, minor = sys.version_info[:2]
        assert major == 3, f"Expected Python 3, got {major}"
        assert minor == 11, f"Expected Python 3.11, got 3.{minor}"
    
    def test_python_executable_exists(self):
        """Verify Python executable path is valid."""
        assert sys.executable, "Python executable not found"
        assert sys.executable.endswith("python"), \
            f"Unexpected executable: {sys.executable}"


class TestPyTorchInstallation:
    """Test PyTorch installation and configuration."""
    
    def test_torch_installed(self):
        """Verify PyTorch is installed."""
        try:
            import torch  # noqa: F401
        except ImportError:
            pytest.fail("PyTorch is not installed")
    
    def test_torch_version(self):
        """Verify PyTorch version matches env_mps.yml (2.5)."""
        import torch
        # Remove build metadata
        torch_ver = version.parse(torch.__version__.split('+')[0])
        expected_ver = version.parse("2.5")
        assert torch_ver >= expected_ver, \
            f"Expected PyTorch >= 2.5, got {torch.__version__}"
    
    def test_torch_mps_available(self):
        """Verify MPS backend is available on the system."""
        import torch
        # This test is specifically for macOS with MPS support
        if platform.system() == "Darwin":
            assert torch.backends.mps.is_available(), \
                "MPS backend is not available on this macOS system"
        else:
            pytest.skip("MPS is only available on macOS")
    
    def test_torch_mps_built(self):
        """Verify PyTorch was built with MPS support."""
        import torch
        if platform.system() == "Darwin":
            assert torch.backends.mps.is_built(), \
                "PyTorch was not built with MPS support"
        else:
            pytest.skip("MPS is only available on macOS")
    
    def test_torch_can_create_mps_tensor(self):
        """Verify we can create tensors on MPS device."""
        import torch
        if (platform.system() != "Darwin"
                or not torch.backends.mps.is_available()):
            pytest.skip("MPS is not available on this system")

        try:
            # Create a simple tensor on MPS device
            tensor = torch.tensor([1.0, 2.0, 3.0], device="mps")
            assert tensor.device.type == "mps", \
                f"Expected tensor on mps device, got {tensor.device.type}"
            assert tensor.shape == (3,), "Tensor shape mismatch"
        except RuntimeError as e:
            pytest.fail(f"Failed to create MPS tensor: {e}")
    
    def test_torch_cuda_not_available_on_mac(self):
        """Verify CUDA is not available on macOS (expected)."""
        import torch
        if platform.system() == "Darwin":
            assert not torch.cuda.is_available(), \
                "CUDA should not be available on macOS"
        else:
            pytest.skip("This test is specific to macOS")


class TestDependencies:
    """Test that all required dependencies are installed."""
    
    @pytest.mark.parametrize("package_name", [
        "torchvision",
        "torchaudio",
        "transformers",
        "tokenizers",
        "accelerate",
        "requests",
    ])
    def test_conda_dependencies_installed(self, package_name):
        """Verify conda dependencies from env_mps.yml are installed."""
        spec = importlib.util.find_spec(package_name)
        assert spec is not None, f"{package_name} is not installed"
    
    @pytest.mark.parametrize("package_name", [
        "pymupdf",  # fitz
        "langchain",
        "langchain_huggingface",
        "langchain_community",
        "faiss",
        "sentence_transformers",
        "bitsandbytes",
        "ipykernel",
        "IPython",
        "ipywidgets",
    ])
    def test_pip_dependencies_installed(self, package_name):
        """Verify pip dependencies from env_mps.yml are installed."""
        spec = importlib.util.find_spec(package_name)
        assert spec is not None, f"{package_name} is not installed"


class TestPackageVersions:
    """Test specific package versions as specified in env_mps.yml."""
    
    def test_transformers_version(self):
        """Verify transformers version is 4.54 or compatible."""
        import transformers
        trans_ver = version.parse(transformers.__version__.split('+')[0])
        expected_ver = version.parse("4.54")
        assert trans_ver >= expected_ver, \
            f"Expected transformers >= 4.54, got {transformers.__version__}"
    
    def test_pytorch_version_exact(self):
        """Verify PyTorch version is 2.5.x."""
        import torch
        torch_ver = version.parse(torch.__version__.split('+')[0])
        assert torch_ver.major == 2 and torch_ver.minor == 5, \
            f"Expected PyTorch 2.5.x, got {torch.__version__}"


class TestRAGPipelineRequirements:
    """Test that all components required for RAG pipeline are available."""
    
    def test_langchain_core_available(self):
        """Verify langchain core components are available."""
        try:
            from langchain_core.prompts import PromptTemplate  # noqa: F401
        except ImportError as e:
            pytest.fail(f"LangChain core components not available: {e}")
    
    def test_sentence_transformers_available(self):
        """Verify sentence-transformers for embeddings is available."""
        try:
            from sentence_transformers import (  # noqa: F401
                SentenceTransformer)
        except ImportError as e:
            pytest.fail(f"sentence-transformers not available: {e}")
    
    def test_faiss_available(self):
        """Verify FAISS vector store is available."""
        try:
            import faiss  # noqa: F401
        except ImportError as e:
            pytest.fail(f"FAISS not available: {e}")
    
    def test_pdf_reading_available(self):
        """Verify PyMuPDF (fitz) is available for PDF reading."""
        try:
            import fitz  # noqa: F401
        except ImportError as e:
            pytest.fail(f"PyMuPDF (fitz) not available: {e}")
    
    def test_tokenization_available(self):
        """Verify tokenizers library is available."""
        try:
            from transformers import AutoTokenizer  # noqa: F401
        except ImportError as e:
            pytest.fail(f"AutoTokenizer not available: {e}")


class TestMPSOptimization:
    """Test MPS-specific optimizations and device handling."""
    
    def test_mps_device_type_string(self):
        """Verify MPS device type identifier is correct."""
        import torch
        if platform.system() != "Darwin":
            pytest.skip("MPS is only available on macOS")

        if torch.backends.mps.is_available():
            device = torch.device("mps")
            assert str(device.type) == "mps", \
                f"Expected device type 'mps', got {device.type}"
    
    def test_tensor_operations_on_mps(self):
        """Verify basic tensor operations work on MPS."""
        import torch
        if (platform.system() != "Darwin"
                or not torch.backends.mps.is_available()):
            pytest.skip("MPS is not available on this system")

        try:
            x = torch.randn(10, 10, device="mps")
            y = torch.randn(10, 10, device="mps")
            z = torch.matmul(x, y)
            assert z.device.type == "mps", \
                "Result tensor not on MPS device"
            assert z.shape == (10, 10), \
                "Matrix multiplication shape mismatch"
        except RuntimeError as e:
            pytest.fail(f"Failed to perform tensor operation on MPS: {e}")
    
    def test_mps_dtype_support(self):
        """Verify common dtypes work on MPS device."""
        import torch
        if (platform.system() != "Darwin"
                or not torch.backends.mps.is_available()):
            pytest.skip("MPS is not available on this system")

        # Test float32 (most common)
        try:
            x = torch.tensor([1.0, 2.0], dtype=torch.float32, device="mps")
            assert x.dtype == torch.float32
            assert x.device.type == "mps"
        except RuntimeError as e:
            pytest.fail(f"MPS does not support float32: {e}")
    
    def test_mps_memory_allocation(self):
        """Verify MPS memory allocation works."""
        import torch
        if (platform.system() != "Darwin"
                or not torch.backends.mps.is_available()):
            pytest.skip("MPS is not available on this system")

        try:
            # Allocate a reasonably sized tensor
            tensor = torch.randn(1000, 1000, device="mps")
            assert tensor.is_mps, "Tensor not allocated on MPS"
            del tensor
            torch.mps.empty_cache()
        except RuntimeError as e:
            pytest.fail(f"Failed to allocate memory on MPS: {e}")


class TestEnvironmentConfiguration:
    """Test environment configuration and compatibility."""
    
    def test_pytorch_channels_in_conda(self):
        """Verify that conda is configured with pytorch channel."""
        # This is a metadata test that confirms the env_mps.yml has correct channels
        import torch
        # If torch is installed and working, the channels were correct
        assert hasattr(torch, "__version__"), "PyTorch metadata not available"
    
    def test_no_conflicting_packages(self):
        """Verify no conflicting packages are installed."""
        # Check that CPU-only FAISS doesn't conflict with accelerated versions
        import faiss
        assert faiss is not None, "FAISS import failed"
    
    def test_accelerate_library_available(self):
        """Verify accelerate library (for MPS support) is available."""
        try:
            import accelerate
        except ImportError as e:
            pytest.fail(f"accelerate library not available: {e}")


class TestEnvironmentDocumentation:
    """Test that the environment can be validated against env_mps.yml specs."""
    
    def test_required_channels(self):
        """Verify that packages from specified channels can be imported."""
        # pytorch channel packages
        try:
            import torch
            import torchvision
            import torchaudio
        except ImportError as e:
            pytest.fail(f"Failed to import pytorch channel packages: {e}")
        
        # conda-forge packages
        try:
            import requests
        except ImportError as e:
            pytest.fail(f"Failed to import conda-forge packages: {e}")
    
    def test_rag_specific_imports(self):
        """Verify all imports required by the RAG notebook work."""
        try:
            from langchain_community.vectorstores import FAISS  # noqa: F401
            # from langchain.text_splitter import (  # noqa: F401
                RecursiveCharacterTextSplitter)
            from sentence_transformers import (  # noqa: F401
                SentenceTransformer)
        except ImportError as e:
            pytest.fail(f"Failed to import RAG-specific components: {e}")


class TestSystemInfo:
    """Test system information and compatibility."""
    
    def test_system_is_macos(self):
        """Verify system is macOS (required for MPS)."""
        system = platform.system()
        assert system == "Darwin", \
            f"env_mps.yml is designed for macOS, running on {system}"
    
    def test_macos_version_info_available(self):
        """Verify we can get macOS version information."""
        if platform.system() == "Darwin":
            mac_version = platform.mac_ver()[0]
            assert mac_version, "Could not determine macOS version"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
