# How-To Guides: Applying the Unified AI Governance & Project-Management Framework

These how-to guides address specific situations you may encounter while implementing the integrated AI governance system. Each guide is problem-oriented, providing practical steps, decision trees, and troubleshooting tips.

## 1. Choosing the Right AI Method

### Decision Tree for Selecting AI vs Automation

```mermaid
graph TD
    A[Define business problem] --> B{Rule-based solution possible?}
    B -- Yes --> C[Use traditional automation or analytics]
    B -- No --> D{Structured data available?}
    D -- No --> E[Consider generative AI for unstructured data]
    D -- Yes --> F{Labelled data available?}
    F -- Yes --> G[Supervised learning (e.g., classification/regression)]
    F -- No --> H[Consider unsupervised or semi-supervised learning]
```

#### Guidance

- If rule-based logic can achieve the desired outcome, avoid unnecessary AI.
- Use generative AI only when unstructured data (text, images) must be synthesized; ensure adherence to generative‑AI governance (hallucination mitigation, provenance).
- For high‑risk decisions (e.g., credit scoring, medical diagnoses), adopt supervised models with explainability and human oversight.

## 2. Managing High-Risk AI in Finance

High-risk AI systems (e.g., credit scoring, fraud detection) require stringent controls under the EU AI Act and domain regulations (GLBA, SR 11-7). Here's how to proceed:

1. **Classify the system:** classify as high-risk and register with authorities if required (EU AI Act). Determine whether it is a general-purpose AI model or specific to finance.
2. **Establish accountability structures:** assign a risk officer; ensure the AGC oversees model design and monitoring.
3. **Perform impact assessments:** measure potential harm to consumers; set risk tolerance (impact × likelihood).
4. **Implement fairness & bias checks:** detect disparate impact across protected classes; document mitigation strategies.
5. **Provide explainability:** adopt models that can produce clear explanations; share them with customers and regulators.
6. **Continuous monitoring:** set performance and fairness KPIs; review incidents; schedule audits.

## 3. Deploying Generative AI Responsibly

When integrating generative AI for text generation, summarization, or code suggestion, follow these steps:

1. **Scope the use case:** confirm it falls into an approved category; avoid prohibited practices such as deepfake creation without consent.
2. **Verify training data provenance and licensing:** check for copyrighted material.
3. **Implement content-safety filters:** mitigate hallucinations and harmful outputs. Use alignment tuning and human feedback.
4. **Establish content provenance & watermarking:** track outputs and align with governance recommendations.
5. **Audit outputs regularly:** require human review before external release.
6. **Incident reporting:** set up a process to handle erroneous or harmful content; update models accordingly.

## 4. Aligning with Federal Contracting Requirements

AI projects for federal agencies must comply with FAR/DFARS, NIST SP 800-53, and agency-specific AI policies.

1. **Security & privacy:** implement controls (access management, encryption); align with NIST privacy guidance.
2. **Supply-chain management:** evaluate third-party vendors; ensure AI tools meet cybersecurity and provenance requirements.
3. **Transparency & auditability:** maintain detailed documentation (algorithmic methodology, testing results); provide audit trails for procurement processes.
4. **Ethics & fairness:** integrate bias mitigation strategies; follow agency ethics policies.
5. **Reporting & oversight:** maintain risk registers; prepare periodic reports for contracting officers; participate in reviews.

## 5. Troubleshooting Integration Conflicts

### Problem: Data Quality Issues Discovered Late
- **Symptom:** During model training, critical features are missing or inconsistent.
- **Resolution:** Revisit the Data Understanding phase; update the data inventory; engage data stewards; apply data cleaning and augmentation procedures. Use the readiness assessment to flag future weaknesses.

### Problem: Model Fails Go/No-Go Due to High Risk
- **Symptom:** Impact × likelihood scores exceed risk tolerance.
- **Resolution:** Consider alternative algorithms or model architectures; reduce scope; introduce more human oversight; revisit Business Understanding to reassess objectives.

### Problem: Compliance Uncertainty for GPAI Models
- **Symptom:** Unclear whether a model is considered a general-purpose AI (GPAI) under EU rules.
- **Resolution:** Consult legal counsel; document functional scope; if uncertain, err on the side of applying GPAI obligations—transparency documentation, codes of practice, and voluntary testing.

### Problem: Stakeholder Resistance
- **Symptom:** End users or leadership resist AI adoption due to fear of replacement or mistrust.
- **Resolution:** Use The Fifth Discipline's shared vision and team learning to cultivate buy-in. Conduct workshops; emphasize AI's augmentative role; involve stakeholders in the Map function to surface concerns and design solutions.

## 6. Creating a Project-Specific AI Governance Plan

Follow PMI's AI governance plan structure:

- **Purpose:** articulate why AI governance is needed for the project.
- **Governance principles:** list ethical principles (transparency, fairness, bias mitigation, privacy, accountability) and definitions.
- **Roles & responsibilities:** specify AGC, PMO, and CoE roles; describe collaboration and decision flow.
- **Readiness & maturity assessments:** perform and document results.
- **Use cases & restrictions:** define tasks AI can and cannot perform; list guidelines.
- **Inventory & intake:** maintain a catalogue of approved tools; define intake procedure.
- **Monitoring & risk management:** set KPIs and tracking mechanisms; create a risk table.
- **Data governance:** address data quality, privacy, and security.
- **Alignment with existing policies:** map intersections and fill gaps.
- **Consequences of non-compliance:** outline penalties and reporting.
- **Review & update mechanisms:** schedule reviews and continuous improvement.

By following these how-to guides, you can navigate typical challenges and adapt the unified framework to various industries and regulatory environments.
