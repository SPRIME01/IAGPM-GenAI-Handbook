# Mock Evaluation Artifacts

This directory contains sample evaluation artifacts for testing the governance gate locally.

## Files

- `eval_quality.json` - Quality metrics (pass@k scores)
- `eval_fairness.json` - Fairness metrics (subgroup delta, demographic parity)
- `eval_safety.json` - Safety metrics (harmful rate, jailbreak success)
- `eval_drift.json` - Data drift metrics (PSI, KL divergence)

## Usage

Test the governance gate locally:

```bash
python tools/pac_ci.py \
  --config policies/adr-006.embedded-governance.yaml \
  --eval tests/fixtures/mock_artifacts/eval_quality.json \
  --fairness tests/fixtures/mock_artifacts/eval_fairness.json \
  --safety tests/fixtures/mock_artifacts/eval_safety.json \
  --drift tests/fixtures/mock_artifacts/eval_drift.json
```

Expected output: **PASS** (all thresholds met)

## Threshold Reference (from ADR-006)

| Metric | Current Value | Threshold | Status |
|--------|--------------|-----------|--------|
| Quality (pass@5) | 0.84 | ≥ 0.82 | ✅ PASS |
| Fairness (subgroup_delta) | 0.03 | ≤ 0.05 | ✅ PASS |
| Safety (harmful_rate) | 0.002 | ≤ 0.005 | ✅ PASS |
| Drift (PSI) | 0.08 | warn: 0.1, retrain: 0.2 | ✅ PASS |

## Testing Violations

To test CI failure on violations, modify values:

```json
// eval_quality.json - trigger quality violation
{"pass_at_5": 0.75}  // Below 0.82 threshold

// eval_fairness.json - trigger fairness violation
{"subgroup_delta": 0.08}  // Above 0.05 threshold

// eval_safety.json - trigger safety violation
{"harmful_rate": 0.01}  // Above 0.005 threshold
```

## Generating Real Artifacts

Replace these mocks with real evaluation outputs from:

- **Quality**: HumanEval, MBPP, or custom code benchmarks
- **Fairness**: Aequitas, Fairlearn, or custom bias analysis
- **Safety**: Red-teaming tools, Anthropic's harmfulness classifier
- **Drift**: Evidently AI, NannyML, or custom drift detection

See `docs/IAGPM_GenAI_Handbook/Technical/llmops_reference_runbook.md` for evaluation best practices.
