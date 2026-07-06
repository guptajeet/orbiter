import pytest
from backend.chaos.module import chaos_module

def test_chaos_scenario_toggles():
    scenario = "api_provider_down"
    
    # Initially inactive
    assert not chaos_module.is_active(scenario)

    # Enable for 10 seconds
    chaos_module.enable_scenario(scenario, 10)
    assert chaos_module.is_active(scenario)

    # Disable
    chaos_module.disable_scenario(scenario)
    assert not chaos_module.is_active(scenario)

def test_resilience_suite_run():
    # Execute full resilience checks and check summary output
    passed = chaos_module.run_resilience_suite()
    assert passed is True
