class QualityChecker:
    def check_generation(self, prompt: str, response: str) -> dict:
        """Basic quality checks on AI generation"""
        issues = []
        
        if not response or len(response.strip()) < 10:
            issues.append("Response too short")
        
        if len(response) > 10000:
            issues.append("Response exceeds length limit")
        
        if response.lower().startswith("i don't know") or response.lower().startswith("i cannot"):
            issues.append("Response indicates model uncertainty")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "quality_score": max(0.0, 1.0 - (len(issues) * 0.3))
        }

quality_checker = QualityChecker()
