# GitHub Actions CI/CD Setup - Complete Guide

## Overview

This setup provides comprehensive CI/CD testing for the RAG project across three platforms:
- **CPU**: Linux environment (Ubuntu)
- **MPS**: macOS with Apple Silicon GPU support
- **CUDA**: Linux with NVIDIA GPU support

## Files Created

```
.github/
├── workflows/
│   ├── ci.yml                 # Main comprehensive test suite
│   ├── env-test.yml          # Environment file validation
│   ├── quick-test.yml        # Fast feedback tests
│   └── README.md             # Workflows documentation
├── CI_GUIDE.md               # Detailed CI configuration guide
├── BADGES.md                 # CI status badge configuration
└── SETUP.md                  # This file
```

## Quick Start (3 Steps)

### Step 1: Commit and Push Workflows
```bash
cd /path/to/RAG
git add .github/
git commit -m "Add GitHub Actions CI/CD workflows"
git push origin steven
```

### Step 2: Create Pull Request (Optional)
Visit GitHub and create a PR to main/develop to see all workflows run.

### Step 3: Monitor Results
View results in the **Actions** tab of your GitHub repository.

## What Gets Tested

All workflows run the tests defined in `tests/test_env_cuda.py`:

✅ Python 3.12+ verification
✅ PyTorch installation and availability
✅ CUDA/MPS availability checks
✅ Required package imports (transformers, langchain, faiss, etc.)
✅ Basic tensor operations
✅ Device type detection

## Workflow Triggers

| Workflow | Trigger | When It Runs |
|----------|---------|--------------|
| quick-test.yml | Every push/PR | ~3-5 min (fast) |
| ci.yml | Push to main/steven/develop | ~15-20 min (full matrix) |
| env-test.yml | Changes to env_*.yml files | ~10-15 min per environment |

## Platform Coverage

### CPU Environment (env_cpu.yaml)
- Runs on: Ubuntu latest
- PyTorch: CPU-only
- Purpose: Verify CPU-only functionality
- Time: ~5-10 min

### MPS Environment (env_mps.yml)
- Runs on: macOS latest
- PyTorch: MPS (Apple Silicon)
- Purpose: Test macOS compatibility
- Time: ~5-10 min

### CUDA Environment (env_cuda.yml)
- Runs on: Ubuntu latest
- PyTorch: CUDA 12.1 (CPU fallback in CI)
- Purpose: Verify CUDA/GPU code paths
- Time: ~5-10 min

## Environment Details

Each workflow:
1. Sets up Miniconda
2. Creates environment from .yml file
3. Installs pytest
4. Runs all tests
5. Uploads artifacts (if applicable)

### Special Handling

**CUDA Workflow**:
- Runs `conda clean --all --yes` before creating environment
- Prevents cache corruption issues
- Installs PyTorch with CUDA wheels from pip
- Falls back to CPU if needed

**MPS Workflow**:
- Runs on macOS exclusively
- Automatically detects Metal Performance Shaders
- Preserves MPS-specific code paths

**CPU Workflow**:
- Standard PyTorch CPU installation
- Fastest for quick feedback

## Local Verification Before Push

Test locally first to catch issues:

```bash
# Test CPU environment
conda env create -f env_cpu.yaml --name test-cpu
conda activate test-cpu
python -m pytest tests/ -v

# Test CUDA environment (if applicable)
conda env create -f env_cuda.yml --name test-cuda
conda activate test-cuda
python -m pytest tests/ -v

# Test MPS environment (macOS only)
conda env create -f env_mps.yml --name test-mps
conda activate test-mps
python -m pytest tests/ -v
```

## Monitoring & Notifications

### View Results
1. Go to your GitHub repository
2. Click "Actions" tab
3. Select a workflow run
4. Review logs and results

### Enable Notifications
- GitHub default: Email on workflow failure
- GitHub Actions tab: Real-time status
- Optional: Integrate with Slack/Discord

### Status Badges
Add to README.md:
```markdown
[![CI Status](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)
```

See `.github/BADGES.md` for more options.

## Customization

### Add More Tests
1. Create test file: `tests/test_*.py`
2. Follow pytest conventions
3. Workflows auto-discover and run new tests

### Change Trigger Branches
Edit `on:` section in workflow files:
```yaml
on:
  push:
    branches: [ main, develop, custom-branch ]
  pull_request:
    branches: [ main, develop ]
```

### Modify Python Version
Edit setup step:
```yaml
python-version: '3.12'  # Change this
```

### Add More Jobs
Example: Add linting, coverage, security scanning
```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: pip install flake8
    - run: flake8 src/ tests/
```

## Troubleshooting

### Workflow Won't Start
- Check branch protection rules
- Ensure .github/workflows/ files are committed
- Push to trigger branch (main, steven, develop)

### Tests Fail on Specific Platform
- Check logs in Actions tab
- Verify environment file syntax: `conda env export -n rag > test-output.yml`
- Test locally first

### Timeout Issues
- Conda operations can be slow first time
- Workflows typically complete in 15-20 min
- GitHub Actions has 6-hour timeout limit

### Cache Issues
- CUDA workflow includes `conda clean --all --yes`
- Can add similar step to other workflows if needed

### GPU Not Available
- GitHub Actions free tier runs on CPU
- `torch.cuda.is_available()` returns False
- Test ensures CUDA support is compiled, not necessarily available
- This is expected and normal

## Best Practices

✅ **Do**
- Push frequently to get quick feedback
- Run tests locally before push
- Add descriptive commit messages
- Review workflow logs when tests fail
- Keep environment files in sync

❌ **Don't**
- Commit large files to repository
- Use hardcoded paths in workflows
- Skip tests for convenience
- Ignore workflow failures
- Push directly to main without PR

## Performance Tips

1. **Quick Feedback**: Use quick-test.yml for rapid development
2. **Parallel Testing**: ci.yml tests all platforms simultaneously
3. **Caching**: Conda handles package caching automatically
4. **Selective Runs**: Only run env-test.yml when environment files change

## CI/CD Philosophy

This setup follows these principles:

1. **Fast Feedback**: Quick tests on every push (3-5 min)
2. **Comprehensive Coverage**: Full matrix on PR/main push (15-20 min)
3. **Multi-Platform**: Tests CPU, MPS, and CUDA paths
4. **Reproducibility**: Environment files ensure consistency
5. **Transparency**: All logs publicly visible

## Next Steps

1. ✅ Commit all files: `git add .github/`
2. ✅ Push to GitHub: `git push origin steven`
3. ✅ Monitor first run in Actions tab
4. ✅ Add status badges to README.md (see BADGES.md)
5. ✅ Share with team

## Support

For questions or issues:
- Check workflow logs in Actions tab
- Review `.github/CI_GUIDE.md` for detailed troubleshooting
- See `.github/workflows/README.md` for workflow details
- Consult GitHub Actions documentation

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Miniconda Setup Action](https://github.com/conda-incubator/setup-miniconda)
- [pytest Documentation](https://docs.pytest.org/)
- [PyTorch Installation](https://pytorch.org/)

---

**Created**: November 2, 2025
**For**: RAG Project CI/CD
**Platforms**: CPU, MPS, CUDA
**Test Framework**: pytest
**Python Version**: 3.12+
