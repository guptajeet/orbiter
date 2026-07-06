from .analyzer import statistical_analyzer

class WeeklyEvaluationReport:
    def generate(self) -> dict:
        return {
            "match_precision": statistical_analyzer.calculate_average("match_precision"),
            "callback_rate": statistical_analyzer.calculate_average("callback_rate"),
            "email_response_rate": statistical_analyzer.calculate_average("email_response_rate")
        }

evaluation_reporter = WeeklyEvaluationReport()
