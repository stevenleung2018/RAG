# CI Status Badges

You can add these badges to your README.md to show CI status:

## Individual Workflow Badges

```markdown
### CPU Tests
[![CPU Tests](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg?branch=steven&job=test-cpu)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)

### MPS Tests (macOS)
[![MPS Tests](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg?branch=steven&job=test-mps)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)

### CUDA Tests
[![CUDA Tests](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg?branch=steven&job=test-cuda)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)

### Environment Tests
[![Environment Tests](https://github.com/stevenleung2018/RAG/actions/workflows/env-test.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/env-test.yml)

### Quick Tests
[![Quick Tests](https://github.com/stevenleung2018/RAG/actions/workflows/quick-test.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/quick-test.yml)
```

## Combined Status Badge

```markdown
[![CI Status](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)
```

## Usage

1. Copy the badge markdown code
2. Paste into your README.md file
3. Update the `branch=steven` parameter if using a different branch
4. The badge will automatically show green (✅) or red (❌) based on the latest workflow status

## Example README Section

```markdown
## Status

[![CI Status](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/ci.yml)
[![Quick Tests](https://github.com/stevenleung2018/RAG/actions/workflows/quick-test.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/quick-test.yml)
[![Environment Tests](https://github.com/stevenleung2018/RAG/actions/workflows/env-test.yml/badge.svg?branch=steven)](https://github.com/stevenleung2018/RAG/actions/workflows/env-test.yml)
```
