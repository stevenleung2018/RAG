# GitHub Actions CI Configuration

This document explains the CI/CD workflows configured for the RAG project.

## Workflows Overview

### 1. **ci.yml** - Comprehensive Platform Tests
- **Triggers**: Push to `main`, `steven`, `develop` branches; PRs to `main`, `develop`
- **Jobs**:
  - `test-cpu`: Tests on Ubuntu with CPU-only PyTorch
  - `test-mps`: Tests on macOS with MPS (Apple Silicon GPU)
  - `test-cuda`: Tests on Ubuntu with CUDA PyTorch
  - `lint`: Python code quality checks (black, flake8, pylint)

**Use case**: Full matrix testing across all platforms

### 2. **env-test.yml** - Environment Validation
- **Triggers**: Changes to environment files (`env_*.yml`, `env_*.yaml`)
- **Jobs**:
  - `test-env-cpu`: Validates `env_cpu.yaml`
  - `test-env-mps`: Validates `env_mps.yml`
  - `test-env-cuda`: Validates `env_cuda.yml`
  - `run-test-suite-cuda`: Runs full test suite if CUDA env is valid

**Use case**: Ensures environment files are always valid

### 3. **quick-test.yml** - Fast CI
- **Triggers**: Every push and PR
- **Job**: Single job that runs tests with CPU-only PyTorch (fast)
- **Features**: Uploads test results as artifacts

**Use case**: Quick feedback during development

## Environment File Mapping

| File | Platform | PyTorch | CUDA | MPS | CPU |
|------|----------|---------|------|-----|-----|
| `env_cpu.yaml` | Linux/Windows/Mac | CPU | ❌ | ❌ | ✅ |
| `env_mps.yml` | macOS only | Metal Performance Shaders | ❌ | ✅ | ✅ |
| `env_cuda.yml` | Linux/Windows | CUDA 12.1 | ✅ | ❌ | ✅ |

## How CI Works

### On Every Push
1. `quick-test.yml` runs (fast, CPU-only)
2. Provides immediate feedback

### On Environment File Changes
1. `env-test.yml` runs
2. Tests each environment independently
3. Runs full test suite if all environments are valid

### On PR to main/develop
1. All three workflows run in parallel
2. Tests on CPU, MPS, and CUDA
3. Linting checks run
4. All must pass before merge

## Local Testing

### Test CPU Environment
```bash
conda env create -f env_cpu.yaml
conda activate rag
python -m pytest tests/ -v
```

### Test MPS Environment (macOS only)
```bash
conda env create -f env_mps.yml
conda activate rag
python -m pytest tests/ -v
```

### Test CUDA Environment
```bash
conda env create -f env_cuda.yml
conda activate rag_cuda_test
python -m pytest tests/ -v
```

## Test Coverage

The test suite includes:
- ✅ Python version verification (3.12+)
- ✅ PyTorch installation and CUDA support detection
- ✅ MPS availability check
- ✅ Required package imports
- ✅ Basic tensor operations
- ✅ Device type detection (CUDA/MPS/CPU)

## Troubleshooting

### If CUDA environment fails to create
- The workflow automatically runs `conda clean --all --yes`
- This clears corrupted package cache
- If it still fails, check for NumPy 1.x vs 2.x compatibility (FAISS requirement)

### If tests fail on a specific platform
- Check the workflow logs in GitHub Actions
- The `--tb=short` flag limits traceback verbosity
- Artifacts are uploaded for inspection

### Skipping CI
- Add `[skip ci]` to commit message to skip all workflows
- Add `[skip test]` to skip only test workflows

## Customization

### Adding New Tests
1. Add test file to `tests/` directory
2. Follow naming convention: `test_*.py`
3. Workflows will automatically discover and run them

### Modifying Triggers
Edit the `on:` section in any workflow file:
```yaml
on:
  push:
    branches: [ main, develop ]  # Add/remove branches
  pull_request:
    branches: [ main, develop ]
```

### Adding Notifications
Use GitHub Actions notifications or integrate with Slack/Discord using third-party actions.

## Performance Considerations

- **CPU tests**: ~5-10 minutes
- **MPS tests**: ~5-10 minutes  
- **CUDA tests**: ~5-10 minutes (no actual GPU available in free tier)
- **Quick tests**: ~3-5 minutes
- **Total time for all workflows**: ~15-20 minutes

## Next Steps

1. Push workflows to GitHub
2. Create a PR to verify all workflows run
3. Merge to main branch
4. Monitor workflow runs in GitHub Actions tab

## Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Miniconda Setup Action](https://github.com/conda-incubator/setup-miniconda)
- [Pytest Documentation](https://docs.pytest.org/)
