class OrbiterException(Exception):
    """Base exception for Orbiter"""
    pass

class ConfigurationError(OrbiterException):
    """Raised when configuration is invalid"""
    pass

class ProviderError(OrbiterException):
    """Raised when an AI provider fails"""
    pass

class AdapterError(OrbiterException):
    """Raised when an ATS adapter fails"""
    pass

class PluginError(OrbiterException):
    """Raised when a plugin fails to load or execute"""
    pass

class RateLimitError(ProviderError):
    """Raised when rate limited by a provider"""
    pass

class AllProvidersFailedError(ProviderError):
    """Raised when all AI providers fail"""
    pass
