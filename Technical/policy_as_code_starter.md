# Policy‑as‑Code Starter Pack

## 1. Objective
Transform AI governance requirements into executable checks and automated policy controls.

---

## 2. Governance Scope
Applies to all LLMs, datasets, and integrations managed under the Integrated AI Governance & Project Management System (IAGPM‑GenAI).

---

## 3. Policy Structure
```yaml
rules:
  - id: pii_block_prompt
    description: Block input containing personal data unless lawful basis logged.
    when: prompt.contains_pii == true and lawful_basis == false
    action: block
  - id: jailbreak_detector
    description: Enforce safe mode if jailbreak risk > 0.8.
    when: prompt.jailbreak_score > 0.8
    action: safe_mode
  - id: copyright_guard
    description: Prevent verbatim reproduction of third‑party content > N tokens.
    when: output.verbatim_ratio > 0.2
    action: summarize
```

---

## 4. Evaluation Matrix
| Category | Metric | Threshold | Evidence |
|-----------|---------|-----------|-----------|
| Quality | pass@5 | ≥ 0.82 | Eval suite log |
| Fairness | subgroup delta | ≤ 5 % | Bias report |
| Safety | harmful rate | ≤ 0.5 % | Red‑team report |
| Privacy | re‑ID risk | ≤ 0.1 % | DPIA summary |

---

## 5. Automation Pipeline
1. **Pre‑merge:** run eval suite; fail if thresholds unmet.  
2. **Pre‑prod:** governance gate approval + evidence bundle.  
3. **Prod:** continuous policy monitoring + alerts.  
4. **Post‑incident:** RCA + policy update.

---

## 6. Evidence Bundle Checklist
- Evaluation results (QA, fairness, safety)
- Model & system cards
- DPIA / TRA approvals
- Sign‑offs from Governance Lead + Product Owner

---

## 7. Maintenance Cadence
| Frequency | Task |
|------------|------|
| Weekly | Update block lists & prompt detectors |
| Monthly | Re‑run eval suite & threshold review |
| Quarterly | Policy audit + evidence archival |
| Ad hoc | Incident‑driven policy adjustment |

---

## 8. Outcomes
- Fewer manual reviews per release.  
- Demonstrable traceability of governance controls.  
- Reduced time from policy update to implementation.  
- Audit‑ready evidence pack for NIST AI RMF “Govern” function.
