import re

class Validators:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        pattern = r'^https?://[^\s]+$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Remove potentially dangerous content from text"""
        return text.strip()[:10000] if text else ""

validators = Validators()
