from backend.core.config import settings

class AutomationModeEngine:
    def __init__(self):
        self.config = settings.automation_rules
        self.global_mode = self.config.get("automation_mode", "copilot")
        self.mode_config = self.config.get("mode_config", {})
        self.overrides = self.config.get("agent_overrides", {})

    def can_execute(self, agent_id: str, action: str) -> bool:
        """Determines if an agent is allowed to execute an action based on automation mode"""
        
        # Check if agent has an override
        effective_mode = self.global_mode
        if agent_id in self.overrides:
            effective_mode = self.overrides[agent_id].get("mode", self.global_mode)
            
        # Get permissions for this mode
        permissions = self.mode_config.get(effective_mode, {})
        
        # Return True if allowed, False if requires approval or disabled
        return permissions.get(action, False)
        
    def get_threshold(self) -> float:
        """Get the auto-apply confidence threshold"""
        autopilot_config = self.mode_config.get("autopilot", {})
        return autopilot_config.get("confidence_threshold", 0.80)

mode_engine = AutomationModeEngine()
