from .base import BasePlugin

class PluginValidator:
    @staticmethod
    def validate(plugin_class: type, expected_base: type) -> bool:
        if not issubclass(plugin_class, expected_base):
            return False
        if not getattr(plugin_class, "name", None):
            return False
        return True
