from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.automation_mode import mode_engine
from backend.core.config import settings

router = APIRouter(prefix="/api", tags=["mode"])


class ModeUpdate(BaseModel):
    mode: str


@router.get("/mode")
def get_mode():
    return {
        "current_mode": mode_engine.global_mode,
        "available_modes": ["advisor", "copilot", "autopilot"],
        "mode_config": mode_engine.mode_config,
        "agent_overrides": mode_engine.overrides,
        "confidence_threshold": mode_engine.get_threshold(),
    }


@router.put("/mode")
def update_mode(payload: ModeUpdate):
    valid_modes = ["advisor", "copilot", "autopilot"]
    if payload.mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid mode. Must be one of: {valid_modes}")

    settings.update_config_file("automation_rules.yaml", {"automation_mode": payload.mode})
    mode_engine.global_mode = payload.mode
    return {
        "status": "success",
        "current_mode": payload.mode,
        "confidence_threshold": mode_engine.get_threshold(),
    }
