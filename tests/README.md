# Tests Directory

Comprehensive test suite for the Governed Speed IAGPM-GenAI system.

## Quick Start

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=services --cov=tools --cov-report=html

# Run specific category
pytest tests/unit/ -v          # Fast unit tests
pytest tests/integration/ -v   # Service integration tests
pytest tests/e2e/ -v           # End-to-end workflows
```

## Structure

```
tests/
├── TESTING_GUIDE.md           # Comprehensive testing documentation
├── fixtures/                  # Test data and configurations
│   ├── adr-006.test.yaml     # Test ADR config
│   └── mock_artifacts/       # Sample evaluation JSONs
│       ├── eval_quality.json
│       ├── eval_fairness.json
│       ├── eval_safety.json
│       ├── eval_drift.json
│       └── README.md
├── unit/                      # Unit tests (TODO: implement)
├── integration/               # Integration tests (TODO: implement)
└── e2e/                       # End-to-end tests (TODO: implement)
```

## Testing the Governance Gate Locally

Use the mock artifacts to test `just ci-check`:

```bash
# Copy mock artifacts to expected location
mkdir -p artifacts/
cp tests/fixtures/mock_artifacts/*.json artifacts/

# Run governance gate
just ci-check

# Expected output: Exit code 0 (all thresholds pass)
```

## Current Status

- ✅ Test fixtures and mock artifacts created
- ✅ Testing guide documentation complete
- ❌ Unit tests not yet implemented
- ❌ Integration tests not yet implemented
- ❌ E2E tests not yet implemented

See `.github/PROJECT_STATE.md` Section 1 for test implementation roadmap.

## Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: Complete guide with examples
- **[fixtures/mock_artifacts/README.md](fixtures/mock_artifacts/README.md)**: Mock data usage
- **[../.github/PROJECT_STATE.md](../.github/PROJECT_STATE.md)**: Project roadmap

## Requirements

Install test dependencies:

```bash
pip install pytest pytest-cov pytest-mock requests pyyaml
```

Or use devbox:

```bash
devbox shell
```

## CI Integration

The GitHub Actions workflow (`.github/workflows/governed-speed-ci.yml`) uses these mock artifacts for automated governance gate validation.
