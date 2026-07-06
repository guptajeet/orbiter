import logging
import time

logger = logging.getLogger(__name__)

class ResilienceReport:
    def __init__(self):
        self.start_time = time.time()
        self.results = []

    def record_result(self, scenario: str, status: str, duration: float, error_message: str = ""):
        self.results.append({
            "scenario": scenario,
            "status": status,
            "duration": duration,
            "error_message": error_message
        })

    def print_summary(self):
        logger.info("==============================================")
        logger.info("        ORBITER RESILIENCE SUITE REPORT       ")
        logger.info("==============================================")
        passed = 0
        failed = 0
        for res in self.results:
            status_str = "PASSED" if res["status"] == "pass" else "FAILED"
            logger.info(f"Scenario: {res['scenario']:<20} | Status: {status_str:<6} | Recovery: {res['duration']:.3f}s")
            if res["error_message"]:
                logger.error(f"  -> Error details: {res['error_message']}")
            if res["status"] == "pass":
                passed += 1
            else:
                failed += 1
        logger.info("----------------------------------------------")
        logger.info(f"Total Run: {len(self.results)} | Passed: {passed} | Failed: {failed}")
        logger.info("==============================================")
        return failed == 0

    def get_report_data(self) -> dict:
        passed = sum(1 for r in self.results if r["status"] == "pass")
        failed = len(self.results) - passed
        return {
            "summary": {
                "passed": passed,
                "failed": failed,
                "total": len(self.results)
            },
            "results": [
                {
                    "scenario": r["scenario"],
                    "status": r["status"],
                    "recovery": f"{r['duration']:.3f}s"
                }
                for r in self.results
            ]
        }
