import time
from typing import Dict, Any
from backend.chaos.scenarios import CHAOS_SCENARIOS
from backend.chaos.reporter import ResilienceReport

class ChaosModule:
    def __init__(self):
        self.active_scenarios: Dict[str, dict] = {}
        
    def enable_scenario(self, name: str, duration: int):
        self.active_scenarios[name] = {
            "expires_at": time.time() + duration
        }
        
    def disable_scenario(self, name: str):
        if name in self.active_scenarios:
            del self.active_scenarios[name]
            
    def get_active_scenarios(self):
        now = time.time()
        # Clean expired
        self.active_scenarios = {k: v for k, v in self.active_scenarios.items() if v["expires_at"] > now}
        return self.active_scenarios
        
    def is_active(self, name: str) -> bool:
        self.get_active_scenarios() # trigger cleanup
        return name in self.active_scenarios

    def run_resilience_suite(self):
        report = ResilienceReport()
        print("Starting Chaos Resilience Suite...")
        
        # Test Scenario: api_provider_down
        t0 = time.time()
        try:
            self.enable_scenario("api_provider_down", 5)
            is_active = self.is_active("api_provider_down")
            if is_active:
                status = "pass"
                msg = ""
            else:
                status = "fail"
                msg = "Scenario not activated"
        except Exception as e:
            status = "fail"
            msg = str(e)
        finally:
            self.disable_scenario("api_provider_down")
        report.record_result("api_provider_down", status, time.time() - t0, msg)

        # Test Scenario: api_timeout
        t0 = time.time()
        try:
            self.enable_scenario("api_timeout", 5)
            is_active = self.is_active("api_timeout")
            status = "pass" if is_active else "fail"
            msg = ""
        except Exception as e:
            status = "fail"
            msg = str(e)
        finally:
            self.disable_scenario("api_timeout")
        report.record_result("api_timeout", status, time.time() - t0, msg)
        
        # Test remaining scenarios
        for name in ["api_rate_limited", "redis_outage", "ats_form_change", "all_ai_down"]:
            t0 = time.time()
            try:
                self.enable_scenario(name, 5)
                status = "pass" if self.is_active(name) else "fail"
                msg = ""
            except Exception as e:
                status = "fail"
                msg = str(e)
            finally:
                self.disable_scenario(name)
            report.record_result(name, status, time.time() - t0, msg)

        report.print_summary()
        return report.get_report_data()

chaos_module = ChaosModule()
