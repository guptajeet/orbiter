import pytest
from backend.adapters.registry import adapter_registry
from backend.adapters.greenhouse import GreenhouseAdapter
from backend.adapters.lever import LeverAdapter
from backend.adapters.ashby import AshbyAdapter
from backend.adapters.workday import WorkdayAdapter
from backend.adapters.generic_email import GenericEmailAdapter

def test_adapters_registration():
    # Verify that importing backend.adapters registered the adapters
    gh = adapter_registry.get_adapter("greenhouse")
    assert gh == GreenhouseAdapter

    lv = adapter_registry.get_adapter("lever")
    assert lv == LeverAdapter

    ash = adapter_registry.get_adapter("ashby")
    assert ash == AshbyAdapter

    wd = adapter_registry.get_adapter("workday")
    assert wd == WorkdayAdapter

    em = adapter_registry.get_adapter("email")
    assert em == GenericEmailAdapter

def test_greenhouse_adapter_submit():
    adapter = GreenhouseAdapter()
    res = adapter.submit_application({"job_id": "test_job"}, "resume_data", "cover_letter_data")
    assert res.status == "success"
    assert "Greenhouse" in res.message
    assert res.application_id == "gh_12345"

def test_workday_adapter_submit():
    adapter = WorkdayAdapter()
    
    # Check default submit
    res = adapter.submit_application({"job_title": "Platform Eng", "url": "https://workday.com/jobs/1"}, "resume_data", "cover_letter_data")
    assert res.status == "success"
    assert "Workday" in res.message
    assert res.application_id == "wd_99812"

    # Check CAPTCHA escalation submit
    res_captcha = adapter.submit_application({"job_title": "Platform Eng", "url": "https://workday.com/jobs/1?captcha=1"}, "resume_data", "cover_letter_data")
    assert res_captcha.status == "queued_for_approval"
    assert "CAPTCHA" in res_captcha.message
