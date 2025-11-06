# Model & System Card Templates

## 1. Model Card Template
| Field | Description |
|--------|--------------|
| **Model Name / Version** |  |
| **Purpose / Intended Use** | Define scope, tasks, and limitations. |
| **Out‑of‑Scope Use** | Disallowed applications. |
| **Training Data Sources** | Provenance, licensing, consent basis. |
| **Pre‑processing Steps** | Cleansing, augmentation, labeling. |
| **Model Architecture / Method** | e.g., Transformer, Fine‑tuned LLM, RAG. |
| **Hyperparameters & Hardware** | Training config, compute resources. |
| **Evaluation Datasets & Metrics** | Benchmarks used (Quality, Fairness, Robustness). |
| **Results Summary** | Key metrics with confidence intervals. |
| **Fairness Analysis** | Subgroup performance, bias findings, mitigations. |
| **Safety Testing** | Red‑team coverage, harm types, residual risk. |
| **Privacy Controls** | PII handling, re‑identification risk, logging. |
| **Security Controls** | Access management, adversarial testing, encryption. |
| **Human‑in‑the‑Loop Points** | Review / override steps. |
| **Known Limitations & Caveats** | Failure modes / context constraints. |
| **Monitoring Plan** | KPIs, drift signals, retrain triggers. |
| **Change Log** | Version history with approvals. |

---

## 2. System Card Template
| Field | Description |
|--------|--------------|
| **System Name / Identifier** |  |
| **Owner / Contact** | Responsible organization role. |
| **System Purpose & Functionality** | Overview of AI capabilities. |
| **User Groups & Interfaces** | Internal / external user types + access points. |
| **System Components** | Data sources, models, APIs, orchestration services. |
| **Data Flow Diagram** | High‑level pipeline visualization. |
| **Risk Register Summary** | Top risks, likelihood, impact, mitigations. |
| **Compliance Mappings** | NIST AI RMF, ISO 42001, EU AI Act articles. |
| **Transparency & Disclosure** | User notifications / documentation links. |
| **Human Oversight Mechanisms** | Escalation paths / appeal processes. |
| **Monitoring & Maintenance Plan** | Metrics tracked / frequency / responsible party. |
| **Incident Response Plan** | Workflow summary + contact matrix. |
| **Post‑Market Monitoring / Audit** | Evidence sources & intervals. |
| **Decommissioning / Sunset Procedure** | Data retention + model archival details. |

---

## 3. Example Mermaid Diagram
```mermaid
flowchart LR
  A[User Input] --> B[Pre‑Processing & PII Masking]
  B --> C[LLM Model Inference]
  C --> D[Policy‑as‑Code Filter / Safety Checker]
  D --> E[Response Delivery & Logging]
  E --> F[Monitoring Dashboard / Alerts]
```

---

## 4. Usage Guidelines
1. Complete Model Card before any deployment decision.  
2. System Card must be updated for every integration or significant change.  
3. Store both cards in governance repository for audit and traceability.  
4. Reference cards in EU AI Act evidence pack and ISO 42001 AIMS records.
