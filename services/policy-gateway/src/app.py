from __future__ import annotations

import os
from typing import Dict

from fastapi import Depends, FastAPI

from policy_gateway.application.services import PolicyDecisionService
from policy_gateway.domain.models import (
    CiCheckInput,
    OutputDecisionInput,
    PromptDecisionInput,
)
from policy_gateway.infrastructure.config_file_adapter import ConfigFileAdapter
from policy_gateway.interface.http.schemas import (
    CiCheckRequest,
    CiCheckResponse,
    DecisionResponse,
    OutputCheckRequest,
    PromptCheckRequest,
)

CFG_PATH = os.getenv("PAC_CONFIG", "/config/adr-006.embedded-governance.yaml")


def _build_service() -> PolicyDecisionService:
    configuration_adapter = ConfigFileAdapter(CFG_PATH)
    return PolicyDecisionService(configuration_adapter)


app = FastAPI(title="Policy Gateway")
SERVICE = _build_service()


def get_service() -> PolicyDecisionService:
    return SERVICE


@app.get("/health")
def health(service: PolicyDecisionService = Depends(get_service)) -> Dict[str, str]:
    return service.health()


@app.get("/rules")
def rules(service: PolicyDecisionService = Depends(get_service)) -> Dict[str, object]:
    return service.rules().to_dict()


@app.post("/filter/prompt", response_model=DecisionResponse)
def filter_prompt(
    body: PromptCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> DecisionResponse:
    decision = service.decide_prompt(
        PromptDecisionInput(prompt=body.prompt, context=body.context or {})
    )
    return DecisionResponse(**decision.__dict__)


@app.post("/filter/output", response_model=DecisionResponse)
def filter_output(
    body: OutputCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> DecisionResponse:
    decision = service.decide_output(
        OutputDecisionInput(output=body.output, context=body.context or {})
    )
    return DecisionResponse(**decision.__dict__)


@app.post("/ci/check", response_model=CiCheckResponse)
def ci_check(
    body: CiCheckRequest,
    service: PolicyDecisionService = Depends(get_service),
) -> CiCheckResponse:
    result = service.ci_check(
        CiCheckInput(
            quality=body.quality,
            fairness=body.fairness,
            safety=body.safety,
            drift=body.drift,
        )
    )
    return CiCheckResponse(**result.__dict__)
