# EU AI Act Risk Tier ↔ NIST Control Mapper

## 1. Purpose
Translate EU AI Act risk classification requirements into corresponding NIST AI RMF control areas to support dual compliance assessments.

---

## 2. Mapping Table
| EU AI Act Risk Tier | Key Obligations | NIST AI RMF Functions / Categories | Evidence Artifacts |
|----------------------|-----------------|------------------------------------|--------------------|
| **Prohibited Practices** | Cease development / deployment | Govern → Risk Identification & Management | Risk register decision record |
| **High-Risk Systems** | Risk management system, data governance, technical docs, record keeping, transparency, human oversight, accuracy, robustness, cybersecurity | Govern / Map / Measure / Manage | Risk Mgmt Plan, DPIA, Model & System Cards, Monitoring Logs |
| **GPAI Models** | Transparency + documentation, post-market monitoring | Govern / Manage | Model Card, Disclosure Statement, Monitoring Dashboard |
| **Limited Risk** | User notification, opt-out mechanism | Govern / Map | Disclosure notice, UI records |
| **Minimal Risk** | Voluntary codes of conduct + transparency best practices | Govern | Ethical policy, training records |

---

## 3. Control Alignment Matrix
| NIST Function | EU AI Act Article / Annex | Control Examples | Evidence Sources |
|----------------|---------------------------|-----------------|-----------------|
| **Govern** | Art 9 – Risk Management System | Define AI policy, roles, RACI | Governance charter, training logs |
| **Map** | Art 10 – Data & Data Governance | Validate data quality, bias mitigation | Data catalog, lineage diagram |
| **Measure** | Art 15 – Accuracy & Robustness | Evaluate performance metrics, stress tests | Eval suite results, fairness report |
| **Manage** | Art 61 – Post-Market Monitoring | Incident response & continuous improvement | Monitoring dashboard, incident register |

---

## 4. Implementation Checklist
- [ ] Classify system risk tier per EU AI Act Annex III.  
- [ ] Map each obligation to NIST function and document control owner.  
- [ ] Integrate evidence artifacts into AIMS repository.  
- [ ] Review alignment quarterly and after regulatory updates.

---

## 5. Benefits
- Streamlines compliance with both EU AI Act and NIST AI RMF.  
- Reduces audit effort through shared evidence.  
- Enables cross-functional visibility of risk tier controls.