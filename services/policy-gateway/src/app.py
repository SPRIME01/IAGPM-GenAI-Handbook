from fastapi import FastAPI
from pydantic import BaseModel
import os, json, yaml

app = FastAPI(title="Policy Gateway")

CFG_PATH = os.getenv("PAC_CONFIG", "/config/adr-006.embedded-governance.yaml")
UPSTREAM = os.getenv("PAC_UPSTREAM_URL", "http://localhost:8000")


def load_cfg():
    try:
        if CFG_PATH.endswith((".yml", ".yaml")):
            return yaml.safe_load(open(CFG_PATH))
        return json.load(open(CFG_PATH))
    except Exception:
        return {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rules")
def rules():
    return load_cfg()


class PromptCheckRequest(BaseModel):
    prompt: str
    context: dict | None = None


class OutputCheckRequest(BaseModel):
    output: str
    context: dict | None = None


def decide_prompt(body: PromptCheckRequest, cfg):
    ctx = body.context or {}
    # simple demo logic based on ADR-006 examples
    if ctx.get("contains_pii") and not ctx.get("lawful_basis"):
        return {
            "allowed": False,
            "action": "block",
            "reasons": ["PII without lawful basis"],
        }
    if ctx.get("jailbreak_score", 0) > 0.8:
        return {
            "allowed": True,
            "action": "safe_mode",
            "reasons": ["high jailbreak score"],
        }
    return {"allowed": True, "action": "allow", "reasons": []}


def decide_output(body: OutputCheckRequest, cfg):
    ctx = body.context or {}
    if ctx.get("verbatim_ratio", 0) > 0.2:
        return {
            "allowed": True,
            "action": "summarize",
            "reasons": ["verbatim over limit"],
        }
    return {"allowed": True, "action": "allow", "reasons": []}


@app.post("/filter/prompt")
def filter_prompt(body: PromptCheckRequest):
    return decide_prompt(body, load_cfg())


@app.post("/filter/output")
def filter_output(body: OutputCheckRequest):
    return decide_output(body, load_cfg())


class CiCheckRequest(BaseModel):
    quality: dict
    fairness: dict
    safety: dict
    drift: dict


@app.post("/ci/check")
def ci_check(body: CiCheckRequest):
    cfg = load_cfg()
    viol = []
    if (
        body.quality.get("pass_at_5", 0)
        < cfg["thresholds"]["quality"]["pass_at_5"]["target"]
    ):
        viol.append("quality.pass_at_5")
    if (
        body.fairness.get("subgroup_delta", 1)
        > cfg["thresholds"]["fairness"]["subgroup_delta"]["target_max"]
    ):
        viol.append("fairness.subgroup_delta")
    if (
        body.safety.get("harmful_rate", 1)
        > cfg["thresholds"]["safety"]["harmful_rate"]["target_max"]
    ):
        viol.append("safety.harmful_rate")
    status = "pass" if not viol else "fail"
    return {"status": status, "violations": viol}
