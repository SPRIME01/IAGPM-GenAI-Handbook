# Project development environment

Minimal environment document. See README.md for full developer setup instructions.

## Goals / contract

- Inputs: source files in the repository, a working devbox environment (or a local machine with Python 3.11+).
- Outputs: reproducible dev environment with isolated `.venv`, installed dev dependencies, runnable FastAPI policy gateway, and passing unit tests.
- Error modes: missing `uv` (falls back to `pip`), PEP 668-managed Python (create venv first), missing OS packages for binary wheels.

### Key files & locations

- `services/policy-gateway/src/app.py` — policy gateway FastAPI app.
- `services/policy-gateway/src/policy_gateway/*` — hexagonal architecture code (ports, application, domain, infrastructure, interface).
- `services/policy-gateway/requirements-dev.txt` — development dependencies used by the convenience script.
- `scripts/dev_setup.sh` — convenience script that creates/activates a virtualenv, installs deps (prefers `uv`), runs `ruff` and `pytest`.
- `policies/adr-006.embedded-governance.yaml` — single source of truth for embedded governance thresholds and rules.

### Architecture (high level)

```mermaid
flowchart LR
  subgraph App
    PG[Policy Gateway (FastAPI)]
    PG -->|proxies| vLLM[vLLM / LLM service]
  end

  subgraph K8s[Kubernetes]
    PG_DEPLOY[Deployment: policy-gateway]
    VLLM_DEPLOY[Deployment: vLLM]
    INGRESS[Ingress]
    CONFIGMAP[ConfigMap: adr-006.embedded-governance.yaml]
    PG_DEPLOY -->|mounts| CONFIGMAP
     # Project development environment

     This document describes how to set up and work with the Governed Speed project development environment. It covers the recommended local developer workflow (devbox + virtualenv), the `uv` package manager preference, key environment variables, and quick run/test/lint commands. It also includes mermaid diagrams of the high-level architecture and the developer workflow.

     ## Goals / contract

     - Inputs: source files in the repository, a working devbox environment (or a local machine with Python 3.11+).
     - Outputs: reproducible dev environment with isolated `.venv`, installed dev dependencies, runnable FastAPI policy gateway, and passing unit tests.
     - Error modes: missing `uv` (falls back to `pip`), PEP 668-managed Python (create venv first), missing OS packages for binary wheels.

     ## Key files & locations

     - `services/policy-gateway/src/app.py` — policy gateway FastAPI app.
     - `services/policy-gateway/src/policy_gateway/*` — hexagonal architecture code (ports, application, domain, infrastructure, interface).
     - `services/policy-gateway/requirements-dev.txt` — development dependencies used by the convenience script.
     - `scripts/dev_setup.sh` — convenience script that creates/activates a virtualenv, installs deps (prefers `uv`), runs `ruff` and `pytest`.
     - `policies/adr-006.embedded-governance.yaml` — single source of truth for embedded governance thresholds and rules.

     ## Architecture (high level)

     ```mermaid
     flowchart LR
       subgraph App
         PG[Policy Gateway (FastAPI)]
         PG -->|proxies| vLLM[vLLM / LLM service]
       end

       subgraph K8s[Kubernetes]
         PG_DEPLOY[Deployment: policy-gateway]
         VLLM_DEPLOY[Deployment: vLLM]
         INGRESS[Ingress]
         CONFIGMAP[ConfigMap: adr-006.embedded-governance.yaml]
         PG_DEPLOY -->|mounts| CONFIGMAP
         INGRESS --> PG_DEPLOY
       end

       subgraph Infra
         RES[Risk & Evidence Service]
         PROM[Prometheus]
         GRAF[Grafana]
       end

       PG_DEPLOY --- RES
       PG_DEPLOY --- PROM
       PROM --- GRAF
       VLLM_DEPLOY --- PROM

       note right of PG_DEPLOY
         Gateway runs as a sidecar alongside the LLM in k8s.
         Gateway enforces policies and forwards requests to vLLM.
       end
     ```

     ## Developer workflow (diagram)

     ```mermaid
     flowchart TD
       Devbox[Devbox shell]
       Devbox --> VENV[Create .venv]
       VENV -->|uv present| UV[uv venv .venv]
       VENV -->|uv absent| PYV[python3 -m venv .venv]
       VENV --> Activate[Activate venv]
       Activate --> Install[Install dev deps]
       Install -->|prefer uv| UV_INSTALL[uv install -r requirements-dev.txt]
       Install -->|fallback pip| PIP_INSTALL[pip install -r requirements-dev.txt]
       Install --> Lint[Run ruff]
       Install --> Test[Run pytest]
       Test --> Run[Run uvicorn app:app]
       Run --> Local[Local development / Integration testing]
       CI[GitHub Actions CI] --> Install
       CI --> Lint
       CI --> Test
     ```

     ## Environment variables used by the services

     - `PAC_CONFIG` — path to gateway config (default: `/config/adr-006.embedded-governance.yaml`).
     - `PAC_UPSTREAM_URL` — upstream LLM endpoint (default: `http://localhost:8000`).
     - `STORAGE_PATH` — path for evidence storage (default: `/evidence`).
    - `PAC_LLM_PROVIDER` — select LLM adapter at runtime (default: `http`).
      - `http` — forward to `${PAC_UPSTREAM_URL}`
      - `litellm` — use local `litellm` client adapter (requires package installed)

    ## Streaming SSE endpoint usage

    The Policy Gateway exposes `POST /proxy/completion/stream` which returns a
    Server-Sent-Events stream (`text/event-stream`). Each event contains a
    `data: <chunk>` line and a blank line terminator. Use this endpoint for
    low-latency UI streaming or token-by-token rendering.

    Quick curl test:

    ```bash
    curl -N -H "Content-Type: application/json" \
      -X POST http://localhost:8081/proxy/completion/stream \
      -d '{"prompt":"Summarize the recent meeting notes"}'
    ```

    Browser example using Fetch + ReadableStream (preferred when POST isn't
    supported by EventSource):

    ```javascript
    // POST to an SSE-compatible proxy or use a fetch streaming response
    fetch('/proxy/completion/stream', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: 'Hello' }) })
      .then(resp => {
        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        return reader.read().then(function process({ done, value }) {
          if (done) return;
          const chunk = decoder.decode(value, { stream: true });
          console.log('chunk:', chunk);
          return reader.read().then(process);
        });
      })
      .catch(err => console.error(err));
    ```

    Environment examples:

    ```bash
    # Default (HTTP forwarder)
    export PAC_LLM_PROVIDER=http
    export PAC_UPSTREAM_URL=http://localhost:8000

    # Use litellm adapter (ensure litellm installed in the runtime venv/container)
    export PAC_LLM_PROVIDER=litellm
    ```

     ## Recommended quickstart (zsh / devbox)

     1. Open devbox shell (recommended):

     ```bash
     devbox shell
     ```

     1. Run the convenience setup script (it will create `.venv`, prefer `uv` for installs, and run linter/tests):

     ```bash
     # From the repo root
     chmod +x scripts/dev_setup.sh   # one-time
     ./scripts/dev_setup.sh
     ```

     1. If you want to start the API after setup:

     ```bash
     # Activate the venv created by the script (if not already active)
     source .venv/bin/activate

     # Run the gateway (ensure PYTHONPATH points to the service src dir)
     export PYTHONPATH="$PWD/services/policy-gateway/src:${PYTHONPATH:-}"
     uvicorn app:app --reload --port 8081
     ```

     1. Run a single test file manually (example):

     ```bash

    # Project development environment

    This document describes how to set up and work with the Governed Speed project development environment. It covers the recommended local developer workflow (devbox + virtualenv), the `uv` package manager preference, key environment variables, and quick run/test/lint commands. It also includes mermaid diagrams of the high-level architecture and the developer workflow.

    ## Goals / contract

    - Inputs: source files in the repository, a working devbox environment (or a local machine with Python 3.11+).
    - Outputs: reproducible dev environment with isolated `.venv`, installed dev dependencies, runnable FastAPI policy gateway, and passing unit tests.
    - Error modes: missing `uv` (falls back to `pip`), PEP 668-managed Python (create venv first), missing OS packages for binary wheels.

    ## Key files & locations

    - `services/policy-gateway/src/app.py` — policy gateway FastAPI app.
    - `services/policy-gateway/src/policy_gateway/*` — hexagonal architecture code (ports, application, domain, infrastructure, interface).
    - `services/policy-gateway/requirements-dev.txt` — development dependencies used by the convenience script.
    - `scripts/dev_setup.sh` — convenience script that creates/activates a virtualenv, installs deps (prefers `uv`), runs `ruff` and `pytest`.
    - `policies/adr-006.embedded-governance.yaml` — single source of truth for embedded governance thresholds and rules.

    ## Architecture (high level)

    ```mermaid
    flowchart LR
      subgraph App
        PG[Policy Gateway (FastAPI)]
        PG -->|proxies| vLLM[vLLM / LLM service]
      end

      subgraph K8s[Kubernetes]
        PG_DEPLOY[Deployment: policy-gateway]
        VLLM_DEPLOY[Deployment: vLLM]
        INGRESS[Ingress]
        CONFIGMAP[ConfigMap: adr-006.embedded-governance.yaml]
        PG_DEPLOY -->|mounts| CONFIGMAP
        INGRESS --> PG_DEPLOY
      end

      subgraph Infra
        RES[Risk & Evidence Service]
        PROM[Prometheus]
        GRAF[Grafana]
      end

      PG_DEPLOY --- RES
      PG_DEPLOY --- PROM
      PROM --- GRAF
      VLLM_DEPLOY --- PROM

      note right of PG_DEPLOY
        Gateway runs as a sidecar alongside the LLM in k8s.
        Gateway enforces policies and forwards requests to vLLM.
      end
    ```

    ## Developer workflow (diagram)

    ```mermaid
    flowchart TD
      Devbox[Devbox shell]
      Devbox --> VENV[Create .venv]
      VENV -->|uv present| UV[uv venv .venv]
      VENV -->|uv absent| PYV[python3 -m venv .venv]
      VENV --> Activate[Activate venv]
      Activate --> Install[Install dev deps]
      Install -->|prefer uv| UV_INSTALL[uv install -r services/policy-gateway/requirements-dev.txt]
      Install -->|fallback pip| PIP_INSTALL[pip install -r services/policy-gateway/requirements-dev.txt]
      Install --> Lint[Run ruff]
      Install --> Test[Run pytest]
      Test --> Run[Run uvicorn app:app]
      Run --> Local[Local development / Integration testing]
      CI[GitHub Actions CI] --> Install
      CI --> Lint
      CI --> Test
    ```

    ## Environment variables used by the services

    - `PAC_CONFIG` — path to gateway config (default: `/config/adr-006.embedded-governance.yaml`).
    - `PAC_UPSTREAM_URL` — upstream LLM endpoint (default: `http://localhost:8000`).
    - `STORAGE_PATH` — path for evidence storage (default: `/evidence`).

    ## Recommended quickstart (zsh / devbox)

    1. Open devbox shell (recommended):

    ```bash
    devbox shell
    ```

    2. Run the convenience setup script (it will create `.venv`, prefer `uv` for installs, and run linter/tests):

    ```bash
    # From the repo root
    chmod +x scripts/dev_setup.sh   # one-time
    ./scripts/dev_setup.sh
    ```

    3. If you want to start the API after setup:

    ```bash
    # Activate the venv created by the script (if not already active)
    source .venv/bin/activate

    # Run the gateway (ensure PYTHONPATH points to the service src dir)
    export PYTHONPATH="$PWD/services/policy-gateway/src:${PYTHONPATH:-}"
    uvicorn app:app --reload --port 8081
    ```

    4. Run a single test file manually (example):

    ```bash
    pytest services/policy-gateway/tests/test_policy_service.py -q
    ```

    ## Using `uv` (package manager)

    - This repository prefers `uv` when available for fast installs and venv management. `scripts/dev_setup.sh` tries `uv` first and falls back to pip.
    - Typical `uv` commands used by the script:
      - `uv venv .venv` — create a venv
      - `uv install -r services/policy-gateway/requirements-dev.txt` or `uv add -r ...` — install requirements

    If `uv` is present on your machine, the script will use it automatically. If not present, the script uses `python3 -m venv` + `pip`.

    ## CI recommendations

    - Add a GitHub Actions workflow to replicate `scripts/dev_setup.sh` steps:
      1. create Python 3.11 environment
      2. create/activate venv or rely on Actions runner's python
      3. install `uv` if you want to use it (optional) or use `pip` to install `requirements-dev.txt`
      4. run `ruff` and `pytest` as part of PR validation

    ## Troubleshooting

    - If the script fails with a PEP 668 / "externally-managed-environment" error, create and activate a venv first:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ./scripts/dev_setup.sh
    ```

    - If imports fail in tests (e.g. `ModuleNotFoundError: No module named 'yaml'`) ensure `PyYAML` is installed in the active venv (the script installs it from `requirements-dev.txt`).

    ## Notes and next steps

    - The repository follows a hexagonal architecture for the policy gateway; domain models and HTTP schemas are kept separate. We added `to_response()` helpers on domain classes to centralize mapping (see `services/policy-gateway/src/policy_gateway/domain/models.py`).
    - You can add a CI job and/or a `Makefile`/`just` entry that wraps `scripts/dev_setup.sh` for a single-command developer experience.

    If you want, I can also:

    - Add a GitHub Actions workflow that runs `scripts/dev_setup.sh` (or equivalent steps) on PRs.
    - Extend the diagrams with more details (Kubernetes manifests, ingress, or observability dashboards).
   1. Run a single test file manually (example):

   ```bash
   pytest services/policy-gateway/tests/test_policy_service.py -q
   ```

### Using `uv` (package manager)

- This repository prefers `uv` when available for fast installs and venv management. `scripts/dev_setup.sh` tries `uv` first and falls back to pip.
- Typical `uv` commands used by the script:
  - `uv venv .venv` — create a venv
  - `uv install -r services/policy-gateway/requirements-dev.txt` or `uv add -r ...` — install requirements

   If `uv` is present on your machine, the script will use it automatically. If not present, the script uses `python3 -m venv` + `pip`.

### CI recommendations

- Add a GitHub Actions workflow to replicate `scripts/dev_setup.sh` steps:
     1. create Python 3.11 environment
     1. create/activate venv or rely on Actions runner's python
     1. install `uv` if you want to use it (optional) or use `pip` to install `requirements-dev.txt`
     1. run `ruff` and `pytest` as part of PR validation

### Troubleshooting

- If the script fails with a PEP 668 / "externally-managed-environment" error, create and activate a venv first:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ./scripts/dev_setup.sh
   ```

- If imports fail in tests (e.g. `ModuleNotFoundError: No module named 'yaml'`) ensure `PyYAML` is installed in the active venv (the script installs it from `requirements-dev.txt`).
