# GitHub Actions Workflows

This directory contains CI/CD workflows for the RAG project.

## Quick Start

The workflows are automatically triggered by:
- Push events to `main`, `steven`, `develop` branches
- Pull requests to `main` and `develop` branches
- Manual trigger via "Run workflow" button

## Workflow Files

1. **ci.yml** - Main comprehensive test suite
   - Tests on CPU (Linux), MPS (macOS), and CUDA (Linux)
   - Includes linting checks

2. **env-test.yml** - Environment file validation
   - Triggered on changes to environment files
   - Tests each environment independently
   - Runs full test suite if all environments valid

3. **quick-test.yml** - Fast feedback workflow
   - Runs on every push/PR
   - Uses CPU-only PyTorch for speed
   - Uploads test artifacts

## Test Results

View test results in the **Actions** tab of your GitHub repository.

Click on any workflow run to see detailed logs and results.

## Skipping Workflows

Add to commit message:
- `[skip ci]` - Skip all workflows
- `[skip test]` - Skip test workflows

## Troubleshooting

See `.github/CI_GUIDE.md` for detailed troubleshooting and customization guide.
