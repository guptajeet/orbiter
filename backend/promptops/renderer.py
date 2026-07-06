from .manager import prompt_manager

class PromptRenderer:
    def render(self, prompt_name: str, **kwargs) -> str:
        pv = prompt_manager.get_active_prompt(prompt_name)
        if not pv:
            raise ValueError(f"No active prompt found for {prompt_name}")
            
        content = pv.content
        for var in pv.variables:
            if var not in kwargs:
                raise ValueError(f"Missing required variable '{var}' for prompt '{prompt_name}'")
            # Simple replacement
            content = content.replace(f"{{{{{var}}}}}", str(kwargs[var]))
            
        return content

prompt_renderer = PromptRenderer()
