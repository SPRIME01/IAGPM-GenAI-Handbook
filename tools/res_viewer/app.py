import os, json, time
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------
# Config
# ----------------------------
RES_URL = os.getenv("RES_URL", "http://localhost:8080")
st.set_page_config(page_title="Risk & Evidence Viewer", layout="wide")


# ----------------------------
# Helpers
# ----------------------------
def get_json(url, default=None):
    try:
        r = requests.get(url, timeout=5)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return default


def post_json(url, payload):
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.ok, r.text
    except Exception as e:
        return False, str(e)


def mock_snapshot():
    return {
        "model_version": "demo-abc123",
        "quality": {"pass_at_5": 0.84},
        "fairness": {"subgroup_delta": 0.03},
        "safety": {"harmful_rate": 0.002},
        "privacy": {"reid_risk": 0.0006},
        "drift": {"psi": 0.08},
        "eu_ai_act_tier": "Limited",
        "timestamp": "2025-11-05T14:32:00Z",
        "evidence_hash": "sha256:demo",
    }


# ----------------------------
# UI
# ----------------------------
st.title("Risk & Evidence Service — Viewer")
st.caption("Visualize governance posture, evidence artifacts, and incidents (ADR-006)")

colA, colB = st.columns([2, 1])
with colA:
    st.subheader("Risk Snapshot")
    model = st.text_input("Model Version (optional):", "")
    url = f"{RES_URL}/risk/snapshot" + (f"?model={model}" if model else "")
    snap = get_json(url, default=mock_snapshot())
    st.json(snap)

    # Gauges (matplotlib)
    df = pd.DataFrame(
        [
            ("pass@5 (↑≥0.82)", snap["quality"]["pass_at_5"]),
            ("fairness Δ (↓≤0.05)", snap["fairness"]["subgroup_delta"]),
            ("harmful rate (↓≤0.005)", snap["safety"]["harmful_rate"]),
            ("re-id risk (↓≤0.001)", snap["privacy"]["reid_risk"]),
            ("drift PSI (warn 0.1)", snap["drift"]["psi"]),
        ],
        columns=["Metric", "Value"],
    )

    st.subheader("Key Metrics")
    st.dataframe(df, use_container_width=True)

    st.subheader("Metric Bars (quick glance)")
    for _, row in df.iterrows():
        label, val = row["Metric"], float(row["Value"])
        fig, ax = plt.subplots()
        ax.bar([label], [val])
        ax.set_ylim([0, max(1.0, val * 1.2)])
        st.pyplot(fig)

with colB:
    st.subheader("Submit Evidence (demo)")
    art_type = st.selectbox(
        "Artifact Type", ["ci_evidence", "eval_pack", "model_card", "dpia"]
    )
    meta = st.text_area("Metadata (JSON)", '{"note":"demo evidence"}')
    if st.button("Post Evidence"):
        ok, resp = post_json(
            f"{RES_URL}/evidence",
            {
                "artifactType": art_type,
                "modelVersion": model or "demo-abc123",
                "metadata": json.loads(meta),
                "contentRef": "s3://demo/bundle/",
            },
        )
        st.success("Posted!") if ok else st.error(resp)

st.markdown("---")
st.caption(f"RES URL: {RES_URL} — set via env var `RES_URL`")
