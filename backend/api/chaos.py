from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.chaos.module import chaos_module
from backend.chaos.scenarios import CHAOS_SCENARIOS

router = APIRouter(prefix="/api", tags=["chaos"])


class ScenarioEnable(BaseModel):
    duration: int = 60


@router.get("/chaos/scenarios")
def list_scenarios():
    active = chaos_module.get_active_scenarios()
    return {
        "scenarios": [
            {
                "name": name,
                "description": info["description"],
                "severity": info["severity"],
                "is_active": name in active,
                "expires_at": active[name]["expires_at"] if name in active else None,
            }
            for name, info in CHAOS_SCENARIOS.items()
        ]
    }


@router.post("/chaos/scenarios/{name}/enable")
def enable_scenario(name: str, payload: ScenarioEnable):
    if name not in CHAOS_SCENARIOS:
        raise HTTPException(status_code=404, detail=f"Unknown scenario: {name}")
    chaos_module.enable_scenario(name, payload.duration)
    return {"status": "enabled", "scenario": name, "duration": payload.duration}


@router.post("/chaos/scenarios/{name}/disable")
def disable_scenario(name: str):
    if name not in CHAOS_SCENARIOS:
        raise HTTPException(status_code=404, detail=f"Unknown scenario: {name}")
    chaos_module.disable_scenario(name)
    return {"status": "disabled", "scenario": name}


@router.post("/chaos/run-suite")
def run_resilience_suite():
    return chaos_module.run_resilience_suite()
