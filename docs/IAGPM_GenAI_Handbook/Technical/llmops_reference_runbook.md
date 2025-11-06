# LLMOps Reference Architecture & Runbook (IAGPM-GenAI)

## 1. Purpose
Provide a repeatable, governed approach for developing, deploying, and maintaining large-language-model (LLM) systems that align with Responsible AI principles and enterprise delivery discipline.

---

## 2. Reference Architecture
```mermaid
flowchart LR
  A[Business Objectives] -->|Phase I – Business Understanding| B[Data Discovery & Legal Basis]
  B -->|Phase II – Data Understanding| C[Data Preparation & Labeling]
  C -->|Phase III – Data Preparation| D[Model Development (Base, FT, RAG)]
  D -->|Phase IV – Model Development| E[Safety & Policy-as-Code Gates]
  E -->|Phase V – Evaluation| F[Evaluation (Quality, Fairness, Robustness)]
  F -->|Go/No-Go| G[Deployment (API, Batch, Agent)]
  G -->|Phase VI – Operationalization| H[Monitoring (Metrics, Drift, Incidents)]
  H --> I[Continuous Improvement & Retraining]
  I --> A
```

---

## 3. Key Roles
| Role | Responsibilities |
|-------|------------------|
| **Product Owner** | Defines business KPIs, approves success criteria |
| **ML Engineer / Data Scientist** | Model dev, evaluation, retraining |
| **MLOps Engineer** | CI/CD, infra, monitoring pipelines |
| **Governance Lead** | Compliance mapping (NIST, ISO, EU AI Act) |
| **Risk Manager** | Maintains risk register, incident response |

---

## 4. Service Level Objectives (SLOs)
| Dimension | Metric | Target |
|------------|---------|---------|
| Latency | p95 < 2 s | ✅ |
| Availability | 99.5 % | ✅ |
| Quality | ≥ 0.82 pass@5 | ✅ |
| Harmful Output Rate | ≤ 0.5 % | ✅ |
| Privacy Incidents | 0 | ✅ |

---

## 5. Pre-Deployment Gates
1. **Documentation Complete:** Model & System Cards.
2. **Evaluation Pass:** Quality/Fairness/Safety thresholds met.
3. **Compliance Check:** DPIA / TRA approved.
4. **Rollback Plan:** Verified last-known-good snapshot.
5. **Stakeholder Sign-off:** Product Owner + Governance Lead.

---

## 6. Monitoring & Retraining Triggers
| Trigger | Threshold | Action |
|----------|------------|---------|
| Data drift (PSI) | > 0.2 | Retrain model |
| Quality drop | > 10 % QoQ | Review dataset + features |
| Incident count | > 3 per month | Launch RCA review |
| Policy update | New law / standard | Re-assess controls |

---

## 7. Incident Response Flow
1. Detect → Contain → Communicate.  
2. Classify: Data breach / Safety failure / Infra error.  
3. Open ticket + notify Risk Manager.  
4. Execute rollback if required.  
5. Complete RCA within 24 h + update playbooks.

---

## 8. Evidence Artifacts
- Governance charter & RACI
- Model card + system card
- Evaluation pack (QA results, fairness tests)
- Monitoring dashboard logs
- Incident register & RCA summaries

---

## 9. Continuous Improvement
Apply Plan-Do-Check-Act:
1. **Plan:** Identify drift / risk / enhancement.
2. **Do:** Implement fix / update model.
3. **Check:** Evaluate against KPIs & thresholds.
4. **Act:** Update policy, documentation, training.