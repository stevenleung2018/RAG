# conftest.py
import os
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--require-cuda",
        action="store_true",
        default=False,
        help="Run CUDA tests that require GPU/drivers."
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "cuda: mark test as requiring CUDA runtime/drivers")

def pytest_collection_modifyitems(config, items):
    run_cuda = config.getoption("--require-cuda")
    if run_cuda:
        return
    skip = pytest.mark.skip(reason="CUDA tests disabled. Use --require-cuda to enable.")
    for item in items:
        if "cuda" in item.keywords:
            item.add_marker(skip)