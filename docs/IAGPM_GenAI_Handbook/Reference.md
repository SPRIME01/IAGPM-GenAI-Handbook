# Reference: Component Catalog & Quick‑Lookup Tables

This reference provides an information‑oriented view of the unified AI governance and project‑management system. Use it as a quick lookup during implementation to understand tasks, artefacts, inputs, outputs and techniques.

## 1. Component Catalog

### 1.1 Phases & Functions

| Phase / Function | Description | Key Artefacts | Inputs | Outputs | Techniques & References |
|---|---|---|---|---|---|
| **Business Understanding** | Define business objectives, decide if AI is appropriate; analyse context & regulations. | Project charter, stakeholder map, legal compliance checklist, ethical principles document | Business problem statement, regulatory landscape, stakeholder expectations | Go/No‑Go decision to proceed; risk appetite matrix | ISO 42001 context analysis, EU AI Act classification, PMI roles & readiness templates |
| **Data Understanding & Map** | Inventory data, assess quality and provenance, map stakeholders and context. | Data inventory, bias analysis report, context map | Existing data sources, data governance policies | Data feasibility assessment, stakeholder impact analysis | Data profiling, bias audits, Map function practices |
| **Data Preparation** | Clean, augment and label data; ensure privacy. | Data‑cards, augmentation logs, labeling guidelines | Raw datasets, privacy requirements | Prepared datasets ready for modelling | Data cleaning, synthetic data generation, privacy‑enhancing technologies |
| **Model Development** | Select algorithms and train models; tune hyper‑parameters. | Experiment logs, model cards, hyper‑parameter records | Prepared data, modelling techniques | Trained models, performance metrics | ML algorithms, generative‑AI safety alignment |
| **Model Evaluation & Measure** | Evaluate models technically and ethically; compute risk metrics. | Evaluation report, fairness/bias report, risk assessment | Trained models, test data, risk tolerance matrix | Go/No‑Go recommendation; approved or rejected model | Performance testing, fairness metrics, risk measurement policies |
| **Operationalization & Manage** | Deploy models, monitor performance and usage, manage incidents. | Deployment plan, monitoring dashboard, risk register, incident reports, decommissioning plan | Approved model, deployment environment, monitoring KPIs | Operational AI system, performance reports, incident handling | MLOps pipelines, monitoring tools, incident response playbooks |
| **Cross‑cutting Functions** | Governance policies, risk management, ethics, data governance. | Policies & procedures manual, training materials, compliance registry | Regulatory standards (GDPR, HIPAA, GLBA), ethical guidelines | Updated policies, compliance reports | Documentation policies, workforce diversity & inclusion programs |

### 1.2 Template Library

| Template | Purpose | Source |
|---|---|---|
| **Readiness Assessment Table** | Measures organizational preparedness; rates areas on 0–3 scale. | PMI AI Governance Plan |
| **Maturity Assessment** | Defines AI integration maturity levels and guides improvements. | PMI |
| **Use Cases & Restrictions Table** | Lists tasks AI can and cannot perform, with guidelines. | PMI |
| **Tool Inventory** | Catalogs approved AI tools; notes training resources and usage guidelines. | PMI |
| **Intake Process Description** | Specifies submission process, evaluation criteria and pilot testing for new tools. | PMI |
| **Monitoring Plan** | Outlines performance and usage monitoring requirements. | PMI |
| **Risk Management Table** | Records risks, severity/likelihood scores, mitigation strategies and responses. | PMI |
| **Data‑card** | Documents dataset details (source, fields, transformations, quality, privacy). | CPMAI + ISO 42001 |
| **Model Card** | Summarizes model purpose, metrics, limitations and bias assessments. | NIST + AI community |

## 2. Quick‑Lookup Tables

### 2.1 Regulations & Frameworks by Industry

| Industry | Key Regulations | Primary Considerations |
|---|---|---|
| **Finance** | EU AI Act (high‑risk classification), GLBA, Basel, SR 11‑7 | Fair lending and anti‑bias audits; explainability of credit decisions; model risk management. |
| **Life Sciences / Healthcare** | EU AI Act, HIPAA/HITECH, FDA SaMD guidance | Patient safety; data privacy; clinical validation; human oversight. |
| **Federal Contracting** | FAR/DFARS, NIST SP 800‑53, agency AI policies | Supply‑chain security; auditability; fairness; compliance with procurement rules. |
| **Technology** | EU AI Act, IP law, open‑source licenses | Transparency of AI models; responsible use of open‑source tools; rapid iteration with governance. |

### 2.2 Mapping CPMAI Phases to AI RMF Functions

| CPMAI Phase | Govern | Map | Measure | Manage | Notes |
|---|---:|---|---|---|---|
| **Business Understanding** | Establish policies, roles and risk appetite. | Identify stakeholders and context. | Define risk tolerance and success metrics. | N/A | ISO 42001 context and EU AI Act classification applied. |
| **Data Understanding** | Ensure data‑governance policies apply. | Map data sources, provenance, stakeholders. | Assess data quality risks and biases. | Document remediation plans. | Use data inventory template. |
| **Data Preparation** | Approve privacy techniques and labeling policies. | N/A | Evaluate data risks after cleaning. | Approve augmentation and transformation; document data‑cards and privacy compliance. |  |
| **Model Development** | Approve model experimentation; ensure accountability. | Validate context alignment. | Measure model risks and performance. | Oversee model management and documentation. | Includes generative‑AI safety alignment. |
| **Model Evaluation** | Conduct Go/No‑Go review. | Check if context assumptions still hold. | Compute final risk scores. | Plan risk responses and incident protocols. | Align with EU AI Act obligations. |
| **Operationalization** | Maintain policies for deployment, monitoring and decommissioning. | Update context maps as environments change. | Monitor risk metrics and model performance. | Manage incidents and retraining cycles. | Implement monitoring and review mechanisms. |

### 2.3 NIST AI RMF Govern Categories (Summary)

- **Govern 1: Policies & processes** — Maintain risk management policies; inventory AI systems; plan decommissioning safely.
- **Govern 2: Accountability structures** — Document roles & responsibilities for mapping, measuring & managing risks; provide training; ensure leadership accountability.
- **Govern 3: Workforce diversity, equity & inclusion** — Engage diverse teams for decision‑making; define human‑AI roles.
- **Govern 4: Culture & values** — Foster safety‑first mindset and document risks and impacts.
- **Govern 5: Engagement with AI actors** — Collect external stakeholder feedback; integrate into design.
- **Govern 6: Third‑party & supply chain** — Address risks from third‑party data/models; plan contingency for failures.

### 2.4 Risk Scoring

To assess risk magnitude, use this simple formula and thresholds:

Risk Score = Severity (0–10) × Likelihood (0–10)

| Risk Level | Score Range | Action |
|---|---:|---|
|**Low** | 0–20 | Acceptable; monitor routinely |
|**Moderate** | 21–50 | Implement mitigation; monitor |
|**High** | 51–79 | Immediate mitigation; restrict use |
|**Critical** | 80–100 | Halt deployment; perform redesign |

This matrix should be customized based on industry and regulatory risk appetite.

## 3. Integration API Specifications (Conceptual)

While no software API is provided here, the unified framework can be implemented via standardized interfaces in your Project Management Information System (PMIS). Recommended API endpoints include:

- **/projects/initiate** — Creates a project with governance metadata (objectives, risk appetite, ethical principles). Requires stakeholder list and regulatory classification.
- **/data/inventory** — Registers data sources with metadata (provenance, quality, bias scores). Supports updates and annotations.
- **/models/register** — Logs models with algorithm type, training data links, model card and risk score.
- **/risks/report** — Submits a risk entry (description, severity, likelihood, mitigation plan). Triggers notifications to AGC.
- **/incidents/report** — Reports incidents and triggers incident management workflow.
- **/monitoring/metrics** — Ingests performance and risk metrics for dashboards and alerts.
- **/governance/review** — Records outcomes of scheduled reviews and updates to policies.

These conceptual endpoints can be implemented via RESTful APIs integrated into existing PMIS tools.

## 4. Artifacts, Inputs & Outputs Overview

| Task | Artifacts Produced | Inputs Required | Outputs Delivered |
|---|---|---|---|
| Stakeholder & context analysis | Context report, stakeholder map | Business objectives, legal/regulatory info | Stakeholder expectations, regulatory checklist |
| Readiness assessment | Completed readiness table | Organizational capabilities, data quality info | Readiness score, improvement plan |
| Risk appetite definition | Risk tolerance matrix | Executive input, regulatory guidance | Thresholds for risk decisions |
| Data inventory | Data inventory table | Data sources, owner info | Data quality analysis, bias analysis |
| Model card creation | Model card | Model, training data, evaluation results | Documented model purpose, performance, limitations |
| Risk register maintenance | Risk log | Identified risks, severity/likelihood scores | Mitigation actions, monitoring frequency |
| Monitoring dashboard | KPI and usage dashboards | Model metrics, logs | Alerts, performance reports |
| Review & update | Review report, updated policies | Feedback, monitoring results | Improved governance plan |

This reference ensures teams can quickly locate critical information, templates and decision aids while working within the unified framework.