# NIST AI RMF ⇄ CPMAI+E Crosswalk Matrix

## 1. Purpose
Map the NIST AI Risk Management Framework (RMF) functions to the CPMAI+E phases to show how AI governance and project delivery interlock.

---

## 2. Alignment Table
| NIST Function | Core Activities | CPMAI+E Phase / Task Group | Key Artifacts |
|---------------|-----------------|-----------------------------|---------------|
| **Govern** | Establish policies, accountabilities, culture of risk management | Phase I – Business Understanding & Domain VI Trustworthy AI | Governance Charter, RACI, Ethics Policy |
| **Map** | Contextualize system, identify risks & stakeholders | Phase I–II – Business & Data Understanding | Risk Register, DPIA/TRA, Data Inventory |
| **Measure** | Quantify and assess risks, metrics, and controls | Phases III–V – Data Prep, Model Dev, Eval | Evaluation Pack, Model Card, Fairness Report |
| **Manage** | Monitor performance, respond to incidents, improve controls | Phase VI – Operationalization & Continuous Improvement | Monitoring Dashboard, Incident Logs, RCA |

---

## 3. Governance Artifacts Cross‑Reference
| Artifact | NIST Function | CPMAI+E Phase | Owner |
|-----------|----------------|---------------|--------|
| Governance Charter | Govern | I | Governance Lead |
| Risk Register | Map | I → II | Risk Manager |
| Data Lineage Diagram | Map / Measure | II → III | Data Engineer |
| Model Card | Measure | V | ML Engineer |
| Evaluation Pack | Measure / Manage | V → VI | QA Lead |
| Monitoring Dashboard | Manage | VI | MLOps Engineer |
| Post‑Market Report | Manage / Govern | VI | Compliance Officer |

---

## 4. Implementation Checklist
- [ ] Map NIST “Govern” outputs to Phase I deliverables (Business Case, Charter).  
- [ ] Embed risk controls in data and model tasks.  
- [ ] Ensure every model has a Model Card + Eval Pack before deployment.  
- [ ] Maintain continuous monitoring logs linked to risk register.  
- [ ] Review all controls quarterly (Plan‑Do‑Check‑Act).

---

## 5. Benefits
- Demonstrates traceable governance across lifecycle.  
- Reduces duplication between risk and project frameworks.  
- Creates audit‑ready evidence aligned to NIST AI RMF and CPMAI+E.  
- Supports enterprise readiness for ISO/IEC 42001 certification.
