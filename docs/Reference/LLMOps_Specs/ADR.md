# ADR-001: Local & Hybrid Kubernetes Deployment

**Status:** Accepted
**Date:** 2025-11-03

## Context
We require a platform-agnostic, reproducible environment for deploying and scaling LLMOps workloads both locally (for development/demo) and in the cloud (for production). The solution must support GPU scheduling, container orchestration, and seamless migration between environments.

## Decision
Adopt **k3s** (lightweight Kubernetes) as the primary orchestration platform for both local and hybrid deployments.

## Options Considered

| Option         | Pros                                         | Cons                        |
|----------------|----------------------------------------------|-----------------------------|
| k3s            | Lightweight, easy local setup, CNCF-compliant| Fewer enterprise features   |
| Kind/minikube  | Good for dev, less production-ready          | Not ideal for prod/hybrid   |
| Managed K8s    | Fully managed, scalable                      | Cost, less local parity     |

## Rationale
k3s provides a minimal, production-grade Kubernetes experience that runs on laptops, workstations, and cloud VMs. This enables rapid prototyping, local testing, and seamless migration to cloud-native environments.

## Consequences
- **Positive:** Unified dev/prod parity, easy demos, low resource usage
- **Negative:** Some advanced K8s features may require workarounds

---

# ADR-002: Automated GitOps Deployment

**Status:** Accepted
**Date:** 2025-11-03

## Context
We need a reproducible, auditable, and automated deployment process for all infrastructure and application components. Manual deployments are error-prone and not scalable.

## Decision
Use **Argo CD** for declarative, GitOps-based continuous deployment to Kubernetes.

## Options Considered

| Option      | Pros                                         | Cons                  |
|-------------|----------------------------------------------|-----------------------|
| Argo CD     | CNCF project, declarative, GitOps, UI/CLI    | Learning curve        |
| Flux        | Also GitOps, good K8s integration            | Smaller ecosystem     |
| Manual      | Simple for small projects                    | Not scalable, error-prone |

## Rationale
Argo CD enables version-controlled, automated, and auditable deployments. It integrates well with k3s and supports both UI and CLI workflows.

## Consequences
- **Positive:** Automated rollouts, rollback, audit trails, easy multi-env management
- **Negative:** Initial setup complexity, requires Git discipline

---

# ADR-003: Scalable LLM Inference Service

**Status:** Accepted
**Date:** 2025-11-03

## Context
The system must serve LLM inference at high throughput (1,000+ req/min), with low latency and support for GPU acceleration. It should be easy to scale horizontally and integrate with orchestration tools.

## Decision
Deploy **vLLM** as the primary LLM inference server, containerized and orchestrated via Kubernetes.

## Options Considered

| Option   | Pros                                         | Cons                  |
|----------|----------------------------------------------|-----------------------|
| vLLM     | High throughput, GPU support, open-source    | Newer project         |
| OpenLLM  | Flexible, supports many models               | Slightly less performant |
| HuggingFace TGI | Mature, good ecosystem                | May require more tuning |

## Rationale
vLLM is optimized for fast, scalable LLM inference and integrates well with Kubernetes-native orchestration. It is proven in production for high-throughput workloads.

## Consequences
- **Positive:** Meets performance targets, easy scaling, modern API
- **Negative:** May require tuning for specific models/hardware

---

# ADR-004: Vector Search Integration

**Status:** Accepted
**Date:** 2025-11-03

## Context
We need to store and retrieve vector embeddings for semantic search and retrieval-augmented generation (RAG). The solution should be open-source, scalable, and easy to integrate with Python and LLM pipelines.

## Decision
Use **pgvector** (PostgreSQL extension) for vector storage and similarity search.

## Options Considered

| Option      | Pros                                         | Cons                  |
|-------------|----------------------------------------------|-----------------------|
| pgvector    | Open-source, SQL, easy integration           | Not as fast as Pinecone for huge scale |
| Pinecone    | Managed, high performance                    | Cost, vendor lock-in  |
| FAISS       | Fast, local, Python-native                   | Not a full DB, less scalable |

## Rationale
pgvector is open-source, integrates with standard PostgreSQL, and is sufficient for most production and demo workloads. It supports SQL queries and is easy to deploy alongside other services.

## Consequences
- **Positive:** Simple deployment, no vendor lock-in, SQL familiarity
- **Negative:** May need to scale up for very large datasets

---

# ADR-005: Observability & Monitoring

**Status:** Accepted
**Date:** 2025-11-03

## Context
Production systems require robust monitoring, logging, and alerting to ensure reliability, performance, and rapid troubleshooting.

## Decision
Adopt **Prometheus** for metrics collection, **Grafana** for dashboards, and centralized logging (e.g., Loki or ELK stack).

## Options Considered

| Option                | Pros                                         | Cons                  |
|-----------------------|----------------------------------------------|-----------------------|
| Prometheus + Grafana  | CNCF standard, K8s-native, flexible          | Some setup required   |
| Datadog/New Relic     | Managed, easy setup                          | Cost, vendor lock-in  |
| Basic K8s metrics     | Built-in, minimal setup                      | Limited functionality |

## Rationale
Prometheus and Grafana are industry standards for Kubernetes observability, providing deep insights and customizable dashboards. They are open-source and widely adopted.

## Consequences
- **Positive:** Full visibility, alerting, open-source, extensible
- **Negative:** Requires initial configuration and resource allocation

---

## References

- [ZenML LLMOps Database]
- [Argo CD GitHub]
- [ZenML Blog: LLMOps in Production]
- [ZenML LLMOps Database: Adept.ai]
- [OpenLLM on Kubernetes]
- [DEV: Scalable Local LLMs]
- [ZenML LLMOps Database: K8s Panel]
- [ZenML Blog: RAG Pipelines]
- [Argo CD Docs]


Here’s an updated **Architecture Decision Record (ADR)** that integrates your article’s core insight (“governance inside the build”) with the governance system from your IAGPM-GenAI framework — blending **CPMAI+E**, **NIST AI RMF**, **ISO 42001**, **EU AI Act**, and **Singapore’s Generative AI model**.
It’s written for **real-world usability** by both technical agents and human reviewers.

---

## Update: LLM adapter & streaming (2025-11-12)

Added runtime wiring for pluggable LLM adapters and a streaming proxy API.

- New environment variable: `PAC_LLM_PROVIDER` — controls which adapter the
   Policy Gateway uses at runtime. Supported values:
   - `http` (default) — forward to an upstream vLLM-like HTTP endpoint
   - `litellm` — use an in-process LiteLLM client adapter when available

- New streaming endpoint (SSE): `POST /proxy/completion/stream` — returns
   Server-Sent-Event formatted chunks from the selected adapter's streaming
   API (useful for low-latency partial responses and UI streaming).

These additions let runtime deployments choose providers by environment and
support streaming without changing application code.

# ADR-006: Embedded AI Governance Integration

**Status:** Accepted
**Date:** 2025-11-05
**Version:** 1.0

---

## Context

Traditional AI projects separate **delivery** (data science, engineering, PMO) from **governance** (risk, legal, ethics).
This creates the “AI speed trap”: models move faster than compliance, leading to post-hoc audits, stalled launches, and reputational damage.

To align safety and speed, the system must **embed governance directly inside the development pipeline**—within data, model, and deployment tasks—rather than treating it as a gate at the end.

The integration follows the **Integrated AI Governance & Project-Management System (IAGPM-GenAI)**, which merges:

* **CPMAI+E** for project lifecycle control
* **NIST AI RMF (Govern–Map–Measure–Manage)** for risk functions
* **ISO 42001** for context, leadership, and continuous improvement
* **EU AI Act** for regulatory classification and transparency
* **Singapore GenAI Framework** for provenance, safety, and incident reporting

---

## Decision

Adopt an **Embedded Governance Architecture (EGA)** where governance tasks are **co-located** with engineering workflows.

| CPMAI Phase                | Embedded Governance Layer                    | Key Controls / Artefacts                                                           |
| -------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Business Understanding** | ISO 42001 context + NIST Govern              | Ethical principles, risk appetite, EU AI Act classification, accountability matrix |
| **Data Understanding**     | NIST Map + Singapore Data Dimension          | Data-card, provenance log, bias & privacy assessments                              |
| **Data Preparation**       | ISO 42001 privacy + PMI Data Governance      | PETs configuration, quality gates, consent validation                              |
| **Model Development**      | NIST Measure + Singapore Trusted Development | Experiment logs, fairness thresholds, auto bias checks                             |
| **Model Evaluation**       | NIST Measure + EU AI Act High-Risk Controls  | Go/No-Go review, model card, explainability audit                                  |
| **Operationalization**     | NIST Manage + Singapore Incident Reporting   | Deployment policy, monitoring dashboard, incident response SOP                     |

**Automation Principle:**
All governance checks are implemented as code where feasible (Policy-as-Code, CI/CD gates, automatic risk scorecard generation).

---

## Options Considered

| Option                                | Pros                                                       | Cons                                            |
| ------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| **Traditional sequential governance** | Familiar to enterprises                                    | Causes delays, audit gaps, “governance theater” |
| **Separate governance pipeline**      | Traceability, modular                                      | Still external to dev flow, low adoption        |
| **Embedded governance (chosen)**      | Continuous assurance, dev-governance parity, self-auditing | Requires culture shift and pipeline refactor    |

---

## Rationale

1. **Resolves timing failure:** governance joins sprints, eliminating hand-offs.
2. **Turns compliance into feedback:** risk metrics appear beside model metrics (e.g., fairness delta, drift score).
3. **Enables audit-by-design:** evidence is version-controlled and reproducible.
4. **Supports regulatory readiness:** EU AI Act & ISO 42001 artefacts generated continuously.
5. **Cultural alignment:** governance becomes part of “Definition of Done.”

---

## Consequences

### Positive

* 30–50 % faster reviews (governance runs in-line)
* Reduced regulatory risk through continuous evidence capture
* Improved trustworthiness metrics (transparency, fairness, explainability)
* Greater cross-team collaboration and reduced friction

### Negative

* Higher initial setup complexity (toolchain & training)
* Requires PMO and risk teams to adopt Agile rituals
* Needs infrastructure for Policy-as-Code and pipeline automation

---

## Implementation Plan

1. **Governance Bootstrapping**

   * Establish AI Governance Committee (AGC) and define roles (PMI template).
   * Approve risk appetite and ethical principles (ISO 42001 context).

2. **Pipeline Instrumentation**

   * Add governance stages to CI/CD:

     * `data_quality_check.py`
     * `bias_scan.yml`
     * `model_card_gen.yml`
     * `risk_scorecard.py`
   * Store results in version-controlled artefacts.

3. **Policy-as-Code**

   * Define YAML/JSON policies for data privacy, model bias, risk thresholds.
   * Integrate with GitOps (Argo CD) for auto rollback on non-compliance.

4. **Monitoring & Incident Response**

   * Prometheus + Grafana dashboards track model KPI + risk KPI.
   * Implement Singapore Model Framework incident reporting triggers.

5. **Continuous Learning**

   * Schedule retros with risk + delivery teams each sprint.
   * Feed lessons into ISO 42001 “Act” cycle.

---

## Governance-in-Delivery Checklist

| Area                  | Example Automation                                          |
| --------------------- | ----------------------------------------------------------- |
| **Data Provenance**   | Data-card auto-generated from ETL metadata                  |
| **Bias Detection**    | CI pipeline runs fairness tests; fails on > Δ threshold     |
| **Explainability**    | SHAP/LIME scores logged; missing explanations flag warnings |
| **Risk Register**     | Risk scores auto-calculated (Impact × Likelihood)           |
| **Incident Response** | Alerts → Jira tickets → post-mortem template                |
| **Audit Trail**       | Model version + risk score stored in Git                    |

---

## Metrics of Success

* ✅ All models produce live risk dashboards
* 🕒 Governance review time < 20 % of total cycle
* 📈 ≥ 90 % compliance evidence auto-generated
* 🧩 Cross-functional participation in > 75 % of sprint reviews
* 💬 Zero post-deployment unreviewed incidents

---

## References

* **CPMAI v7.0 Workbook**, Cognilytica (2023)
* **NIST AI RMF 1.0**, U.S. Dept. of Commerce (2023)
* **ISO/IEC 42001:2024 AI Management System** (AI RMF alignment)
* **Model AI Governance Framework for Generative AI (IMDA, 2024)**
* **AI Governance Plan for Project Management (PMI, 2024)**
* **Integrated AI Governance & Project Management System (Handbook)**

---

