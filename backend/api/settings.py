from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from backend.core.config import settings
from backend.core.action_logger import action_logger

router = APIRouter(prefix="/api", tags=["settings"])


class SettingsUpdate(BaseModel):
    automation_mode: Optional[str] = None
    confidence_threshold: Optional[float] = None
    auto_apply_enabled: Optional[bool] = None
    email_monitoring: Optional[bool] = None
    job_discovery_interval: Optional[int] = None


@router.get("/settings")
def get_settings():
    import os
    from backend.plugins.registry import registry
    
    schedules_config = settings.schedules.get("schedules", {})
    discovery_seconds = schedules_config.get("job_discovery", 7200.0)
    
    provider_keys = {
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    
    # Check AI providers configured status
    ai_providers_status = {}
    for p_name in registry.providers.keys():
        key_var = provider_keys.get(p_name)
        if key_var:
            val = os.environ.get(key_var)
            ai_providers_status[p_name] = bool(val and val != f"your_{p_name}_api_key_here")
        else:
            ai_providers_status[p_name] = True
            
    # Check job sources configured status
    job_sources_status = {}
    for s_name in registry.sources.keys():
        if s_name == "adzuna":
            app_id = os.environ.get("ADZUNA_APP_ID")
            app_key = os.environ.get("ADZUNA_APP_KEY")
            job_sources_status[s_name] = bool(
                app_id and app_id != "your_adzuna_app_id" and
                app_key and app_key != "your_adzuna_app_key"
            )
        elif s_name == "jsearch":
            val = os.environ.get("JSEARCH_API_KEY")
            job_sources_status[s_name] = bool(val and val != "your_jsearch_api_key")
        else:
            job_sources_status[s_name] = True
            
    return {
        "automation_mode": settings.automation_rules.get("automation_mode", "copilot"),
        "confidence_threshold": settings.automation_rules.get("mode_config", {}).get("autopilot", {}).get("confidence_threshold", 0.80),
        "auto_apply_enabled": settings.default_config.get("automation", {}).get("auto_apply", False),
        "email_monitoring": settings.default_config.get("automation", {}).get("email_monitoring", False),
        "job_discovery_interval": int(discovery_seconds / 60.0),
        "ai_providers": ai_providers_status,
        "job_sources": job_sources_status,
    }



@router.put("/settings")
def update_settings(payload: SettingsUpdate):
    from backend.core.automation_mode import mode_engine
    
    updated = {}
    
    if payload.automation_mode is not None:
        settings.update_config_file("automation_rules.yaml", {"automation_mode": payload.automation_mode})
        mode_engine.global_mode = payload.automation_mode
        updated["automation_mode"] = payload.automation_mode
        
    if payload.confidence_threshold is not None:
        settings.update_config_file("automation_rules.yaml", {
            "mode_config": {
                "autopilot": {
                    "confidence_threshold": payload.confidence_threshold
                }
            }
        })
        updated["confidence_threshold"] = payload.confidence_threshold
        
    if payload.auto_apply_enabled is not None:
        settings.update_config_file("default.yaml", {
            "automation": {
                "auto_apply": payload.auto_apply_enabled
            }
        })
        updated["auto_apply_enabled"] = payload.auto_apply_enabled
        
    if payload.email_monitoring is not None:
        settings.update_config_file("default.yaml", {
            "automation": {
                "email_monitoring": payload.email_monitoring
            }
        })
        updated["email_monitoring"] = payload.email_monitoring
        
    if payload.job_discovery_interval is not None:
        interval_seconds = float(payload.job_discovery_interval * 60)
        settings.update_config_file("schedules.yaml", {
            "schedules": {
                "job_discovery": interval_seconds
            }
        })
        updated["job_discovery_interval"] = payload.job_discovery_interval
        
    action_logger.log("settings", "settings_updated", "Dashboard request", f"Updated: {list(updated.keys())}")
    
    return {
        "status": "success",
        "note": "Settings update applied and persisted to configuration files.",
        "updated": updated,
    }


@router.post("/email/check")
def check_email_now():
    try:
        from backend.agents.ingestion.email_monitor import email_monitor_agent
        result = email_monitor_agent.process({"type": "check_inbox"})
        action_logger.log("email_monitor", "email_check", "Manual trigger", f"Result: {result}")
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/email/status")
def email_status():
    token_exists = __import__("os").path.exists("token.json")
    return {
        "gmail_configured": token_exists,
        "note": "First email check will open browser for Google OAuth login" if not token_exists else "Gmail authenticated",
    }
