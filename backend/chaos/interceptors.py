from .module import chaos_module
import time

class ChaosInterceptor:
    """Middleware/Decorator to inject failures"""
    
    @staticmethod
    def intercept_provider(provider_name: str):
        def decorator(func):
            def wrapper(*args, **kwargs):
                import os
                if os.getenv("CHAOS_ENABLED", "false").lower() != "true":
                    return func(*args, **kwargs)
                    
                if chaos_module.is_active("api_provider_down"):
                    # Check if this provider is targeted by the scenario
                    # MVP simplified logic
                    if provider_name == "gemini":
                        raise Exception("Chaos: API Provider Down injected")
                        
                if chaos_module.is_active("api_timeout"):
                    time.sleep(10)
                    
                return func(*args, **kwargs)
            return wrapper
        return decorator
