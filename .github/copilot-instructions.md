# Governed Speed - AI Coding Agent Instructions

## Project Overview

This is an **Integrated AI Governance & Project Management System (IAGPM-GenAI)** - a production-ready framework demonstrating "governed speed": deploying GenAI safely while maintaining compliance with NIST AI RMF, ISO 42001, and EU AI Act.

**Core Architecture**: Policy-as-Code enforcement gateway + Risk & Evidence Service (RES) + Observability stack

## Critical Components

### 1. Policy Gateway (`services/policy-gateway/`)

- **Purpose**: Runtime sidecar enforcing Policy-as-Code rules from `adr-006.embedded-governance.yaml`
- **Key Pattern**: Loads YAML/JSON config at startup, evaluates prompt/output filters via simple rule engine
- **Decision Actions**: `block`, `safe_mode`, `summarize`, `allow`
- **Deployment**: Runs as sidecar container alongside vLLM (see `charts/policy-gateway/templates/deployment.yaml`)

### 2. Risk & Evidence Service (`services/risk-evidence-service/`)

- **Purpose**: Collect evaluation artifacts, expose Prometheus metrics, provide compliance snapshots
- **Storage**: Writes evidence as JSON files to `STORAGE_PATH` with SHA256 hashing
- **Metrics**: Exposes `llm_pass_at_5`, `fairness_subgroup_delta`, `harmful_output_rate`, `drift_psi` via `/metrics`
- **Key Endpoints**: `POST /evidence`, `GET /risk/snapshot`, `POST /incident`

### 3. ADR-006 Configuration (`policies/adr-006.embedded-governance.yaml`)

- **Single Source of Truth** for thresholds and policy rules
- **Structure**: `meta` → `frameworks` → `ownership` → `policy_as_code.rules` → `thresholds`
- **Thresholds Example**: `quality.pass_at_5.target: 0.82`, `fairness.subgroup_delta.target_max: 0.05`
- **Mounted**: As ConfigMap in both gateway and RES containers

## Development Workflows

### Local Development Stack

```bash
# Always use devbox for reproducible environment
devbox shell

# Start full stack (Prometheus + Grafana + pgvector + services)
docker compose -f deployments/docker-compose.yml up --build

# Access:
# - Grafana: http://localhost:3000 (admin/admin)
# - RES API: http://localhost:8080/health
# - Gateway: http://localhost:8081/health
# - Viewer: http://localhost:8501
```

### Pre-Commit Governance Gate

```bash
# Run BEFORE pushing code - enforces thresholds locally
just ci-check

# Requires evaluation artifacts in artifacts/ directory:
# - eval_quality.json (must have pass_at_5)
# - eval_fairness.json (must have subgroup_delta)
# - eval_safety.json (must have harmful_rate)
# - eval_drift.json (must have psi)
```

**Tool**: `tools/pac_ci.py` reads `adr-006.embedded-governance.yaml` and validates metrics against thresholds. Exit code 1 = violations found.

### Kubernetes Deployment

```bash
# 1. Create ADR-006 ConfigMap
kubectl create configmap adr-006-config \
  --from-file=adr-006.embedded-governance.yaml=./policies/adr-006.embedded-governance.yaml \
  -n default

# 2. Deploy via Helm
helm upgrade --install policy-gateway ./charts/policy-gateway -n default
helm upgrade --install risk-evidence-service ./charts/risk-evidence-service -n default
```

### Helm Chart Configuration

**Key Values** (see `charts/*/templates/values.yaml`):

**Policy Gateway**:

- `image.repository`: Container registry path (default: `ghcr.io/your-org/policy-gateway`)
- `targetApp.labels`: Pod selector for vLLM co-location (default: `app: vllm`)
- `targetApp.vllmPort`: vLLM container port (default: `8000`)
- `config.adrConfigCM`: ConfigMap name for ADR-006 (default: `adr-006-config`)
- `resources.limits.memory`: Gateway memory limit (default: `512Mi`)

**Risk & Evidence Service**:

- `storage.size`: PVC size for evidence storage (default: `2Gi`)
- `storage.className`: StorageClass for PVC (set for your cluster)
- `env.STORAGE_PATH`: Evidence file path (default: `/evidence`)
- `ingress.enabled`: Expose RES externally (default: `false`)
- `ingress.host`: DNS for external access (example: `res.localdev`)

**TODO - Expert Guidance**:

- Document recommended StorageClass for production (e.g., `gp3` on EKS, `pd-ssd` on GKE)
- Add secret management pattern for `INCIDENT_WEBHOOK_SECRET` (use SealedSecrets, Vault, or cloud-native solutions)
- Specify OCI registry setup for pushing charts (`helm push` to GHCR or Harbor)
- Add NetworkPolicy examples for restricting gateway→vLLM and RES→pgvector traffic

## Project-Specific Conventions

### Configuration Loading Pattern

Both services use identical config loading:

```python
def load_cfg():
    if CFG_PATH.endswith((".yml", ".yaml")):
        return yaml.safe_load(open(CFG_PATH))
    return json.load(open(CFG_PATH))
```

**Always** support both YAML and JSON formats.

### Environment Variables Standard

- `PAC_CONFIG`: Path to adr-006 config (default: `/config/adr-006.embedded-governance.yaml`)
- `PAC_UPSTREAM_URL`: vLLM endpoint for gateway (default: `http://localhost:8000`)
- `STORAGE_PATH`: Evidence storage location (default: `/evidence`)

### Sidecar Deployment Pattern

The Policy Gateway runs as a **sidecar** container in the same pod as vLLM:

- Gateway listens on port 8081
- vLLM listens on configured `vllmPort` (e.g., 8000)
- Gateway proxies to `http://localhost:{vllmPort}`
- See `charts/policy-gateway/templates/deployment.yaml` for the two-container pattern

### vLLM Integration

**TODO - Expert Guidance Needed**:

- **Current**: Mock vLLM using `http-echo` container in docker-compose
- **Production Pattern**:
  - Use official vLLM image: `vllm/vllm-openai:latest` or specific version
  - Mount model weights via PVC or S3-compatible storage
  - Configure `--model` flag to point to Hugging Face model or local path
  - Set `--api-key` for authentication (store in Kubernetes Secret)
  - Gateway should forward `Authorization: Bearer <token>` headers
  - Example deployment:
    ```yaml
    containers:
      - name: vllm
        image: vllm/vllm-openai:v0.6.0
        command: ["python", "-m", "vllm.entrypoints.openai.api_server"]
        args:
          - --model=/models/llama-3-8b
          - --port=8000
          - --api-key=$(VLLM_API_KEY)
        volumeMounts:
          - name: model-storage
            mountPath: /models
    ```
- **Recommended**: Test with small models like `microsoft/phi-2` or `TinyLlama/TinyLlama-1.1B-Chat-v1.0` before scaling
- **See**: `docker-compose.yml` vllm-mock service for current mock setup

### Evidence Hashing Convention

When storing evidence, always use SHA256 of sorted JSON:

```python
h = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
```

This ensures reproducible hashes for audit trails.

## Key Files to Reference

- **`docs/IAGPM_GenAI_Handbook/Technical/policy_as_code_starter.md`**: Policy rule syntax and enforcement patterns
- **`docs/IAGPM_GenAI_Handbook/Technical/llmops_reference_runbook.md`**: SLOs, gates, incident response flow
- **`specs/openapi-policy-gateway.yaml`**: Complete API contract for gateway
- **`specs/openapi-risk-evidence-service.yaml`**: Complete API contract for RES
- **`observability/grafana/dashboards/dashboard-governed-speed.json`**: Pre-built Grafana dashboard

## Adding New Policy Rules

1. Edit `policies/adr-006.embedded-governance.yaml` → `policy_as_code.rules[]`
2. Add rule with: `id`, `description`, `when` (condition), `action`, `owner`
3. Implement decision logic in `services/policy-gateway/src/app.py` → `decide_prompt()` or `decide_output()`
4. Update ConfigMap: `kubectl delete configmap adr-006-config && kubectl create...`
5. Restart gateway: `kubectl rollout restart deployment/policy-gateway`

## Testing Strategy

### Recommended Test Structure

Create tests following this pattern:

```
tests/
├── unit/
│   ├── test_policy_gateway.py    # Test decide_prompt/decide_output logic
│   ├── test_res_storage.py        # Test evidence hashing/storage
│   └── test_pac_ci.py             # Test threshold validation
├── integration/
│   ├── test_gateway_api.py        # FastAPI TestClient for /filter endpoints
│   ├── test_res_api.py            # Test POST /evidence, GET /risk/snapshot
│   └── test_docker_compose.py     # Health checks on all services
└── fixtures/
    ├── adr-006.test.yaml          # Test config with known thresholds
    └── mock_artifacts/            # Sample eval JSONs for ci-check
```

### Unit Testing Pattern (pytest)

```python
# tests/unit/test_policy_gateway.py
import pytest
from services.policy_gateway.src.app import decide_prompt, PromptCheckRequest

def test_pii_without_lawful_basis_blocks():
    cfg = {"policy_as_code": {"rules": [...]}}  # Load from fixtures
    req = PromptCheckRequest(
        prompt="Contact John at john@example.com",
        context={"contains_pii": True, "lawful_basis": False}
    )
    result = decide_prompt(req, cfg)
    assert result["action"] == "block"
    assert "PII without lawful basis" in result["reasons"]
```

### Integration Testing (Docker Compose)

```python
# tests/integration/test_gateway_api.py
import pytest
import requests

@pytest.fixture(scope="module")
def gateway_url():
    # Assumes docker-compose up running
    return "http://localhost:8081"

def test_filter_prompt_endpoint(gateway_url):
    resp = requests.post(f"{gateway_url}/filter/prompt", json={
        "prompt": "test",
        "context": {"jailbreak_score": 0.9}
    })
    assert resp.status_code == 200
    assert resp.json()["action"] == "safe_mode"
```

### Mock Evaluation Artifacts

Create `tests/fixtures/mock_artifacts/` for `just ci-check`:

```bash
mkdir -p tests/fixtures/mock_artifacts
cat > tests/fixtures/mock_artifacts/eval_quality.json <<'EOF'
{"pass_at_5": 0.84, "pass_at_1": 0.72}
EOF

cat > tests/fixtures/mock_artifacts/eval_fairness.json <<'EOF'
{"subgroup_delta": 0.03, "demographic_parity": 0.95}
EOF

cat > tests/fixtures/mock_artifacts/eval_safety.json <<'EOF'
{"harmful_rate": 0.002, "jailbreak_success": 0.0}
EOF

cat > tests/fixtures/mock_artifacts/eval_drift.json <<'EOF'
{"psi": 0.08, "kl_divergence": 0.05}
EOF
```

Then test locally:

```bash
python tools/pac_ci.py \
  --config policies/adr-006.embedded-governance.yaml \
  --eval tests/fixtures/mock_artifacts/eval_quality.json \
  --fairness tests/fixtures/mock_artifacts/eval_fairness.json \
  --safety tests/fixtures/mock_artifacts/eval_safety.json \
  --drift tests/fixtures/mock_artifacts/eval_drift.json
```

**Current State**: No formal test suite exists yet - validation happens via:

- Docker Compose integration testing (manual)
- `just ci-check` for threshold validation
- Manual API testing via curl/Postman against OpenAPI specs
- GitHub Actions workflow at `.github/workflows/governed-speed-ci.yml`

## Observability

### Prometheus Metrics

RES exposes standard Prometheus client metrics at `/metrics`:

- `res_evidence_events_total` (Counter)
- `llm_pass_at_5` (Gauge)
- `fairness_subgroup_delta` (Gauge)
- `harmful_output_rate` (Gauge)
- `drift_psi` (Gauge)

Scrape config: `observability/prometheus/prometheus.yml`

### Grafana Dashboard

Pre-provisioned dashboard at `observability/grafana/dashboards/dashboard-governed-speed.json` shows:

- Quality/Fairness/Safety/Drift metrics vs thresholds
- Evidence submission timeline
- Incident tracking

## Documentation Framework

The `docs/IAGPM_GenAI_Handbook/` follows **Diátaxis** structure:

- **Tutorial**: Step-by-step learning
- **Howto**: Task-oriented guides
- **Reference**: Technical specifications
- **Explanation**: Conceptual understanding

When updating docs, respect this separation of concerns.

## Common Pitfalls

1. **ConfigMap Updates**: Changes to `adr-006.embedded-governance.yaml` require ConfigMap recreation + pod restart
2. **Port Confusion**: Gateway runs on 8081, vLLM on 8000, RES on 8080 - don't mix them
3. **Devbox Required**: Without `devbox shell`, Python/kubectl/helm versions may mismatch
4. **Evaluation Artifacts**: `just ci-check` fails silently if artifacts/ directory missing - create mock JSONs for testing

## Framework Alignment

All work must align with:

- **CPMAI+E**: Phases I-VI (see `policies/adr-006.embedded-governance.yaml` → `frameworks.cpmai_e`)
- **NIST AI RMF**: Govern-Map-Measure-Manage functions
- **ISO 42001**: AIMS components (Context through Improvement)
- **EU AI Act**: Risk tier classification (default: "Limited")

When adding features, reference the appropriate framework phase/component in commit messages and ADRs.
