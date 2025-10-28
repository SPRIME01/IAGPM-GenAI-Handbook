# Push-Button Kit README (“Governed Speed” Starter Repo)

## 1. Purpose
Provide a ready-to-run reference environment for implementing Responsible AI Governance and LLMOps in 30 days or less.

---

## 2. Folder Structure
```
/governed-speed-kit
 ├── 01_frameworks/           # Core handbook & mappings (NIST, ISO, EU AI Act)
 ├── 02_llmops_runbook/       # Pipelines + monitoring templates
 ├── 03_policy_as_code/       # Executable YAML rules + sample tests
 ├── 04_governance_artifacts/ # Model & System cards + RACI + risk register
 ├── 05_dashboards/           # Executive KPI visuals + balanced scorecard
 ├── 06_training_enablement/  # Slide decks + curriculum modules
 ├── 07_incident_playbooks/   # Response + rollback templates
 └── README.md                # This guide
```

---

## 3. Quick-Start Guide
```bash
# clone the repo
$ git clone https://github.com/org/governed-speed-kit.git

# review core governance docs
$ cd governed-speed-kit/01_frameworks

# simulate policy-as-code checks
$ python simulate_pac.py --input test_prompts.json

# launch dashboard template
$ streamlit run 05_dashboards/app.py
```

---

## 4. Key Components
| Module | Description | Outcome |
|---------|-------------|----------|
| **LLMOps Runbook** | Deploys reference architecture with monitoring + drift alerts | MLOps in compliance mode |
| **Policy-as-Code** | YAML rule engine validates prompts and outputs | Automated safety + privacy checks |
| **Governance Artifacts** | Templates for Model Card, System Card, Risk Register | Audit-ready records |
| **KPI Dashboard** | Streamlit/PowerBI layout for balanced scorecard KPIs | Exec visibility |
| **Training Enablement** | Team and executive curriculum modules | Culture alignment |

---

## 5. Deployment Options
| Environment | Tooling | Recommended Use |
|--------------|----------|----------------|
| Local sandbox | Docker / Streamlit | Demo + training |
| Enterprise CI/CD | Jenkins / GitHub Actions | Policy-as-code validation in pipeline |
| Cloud | Azure / AWS / GCP | Scaled LLMOps deployment |

---

## 6. Configuration Variables
| Variable | Description | Default |
|-----------|-------------|----------|
| POLICY_DIR | Path to YAML rules | ./03_policy_as_code |
| MODEL_REGISTRY | Model storage location | s3://models |
| LOG_LEVEL | Logging verbosity | INFO |
| DASHBOARD_PORT | Port for local UI | 8501 |

---

## 7. Success Criteria
- Repository cloned + run within 15 minutes.  
- 100 % of AI models pass policy gates before deployment.  
- Executive dashboard operational with live KPI feed in ≤ 30 days.