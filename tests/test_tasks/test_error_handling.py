import pytest
from unittest.mock import patch, MagicMock


class TestCeleryConfiguration:
    def test_celery_has_retry_config(self):
        from backend.tasks.celery_app import celery_app
        assert celery_app.conf.task_max_retries == 3
        assert celery_app.conf.task_default_retry_delay == 60
        assert celery_app.conf.task_soft_time_limit == 120
        assert celery_app.conf.task_time_limit == 180

    def test_celery_has_reliability_config(self):
        from backend.tasks.celery_app import celery_app
        assert celery_app.conf.task_acks_late is True
        assert celery_app.conf.task_reject_on_worker_lost is True
        assert celery_app.conf.worker_prefetch_multiplier == 1

    def test_test_task_is_bound(self):
        from backend.tasks.celery_app import test_task
        assert test_task.max_retries == 3
        assert test_task.soft_time_limit == 120
        assert test_task.time_limit == 180


class TestTaskBindings:
    def _check_task(self, task):
        assert task.max_retries == 3
        assert task.soft_time_limit == 120
        assert task.time_limit == 180

    def test_ingestion_tasks_bound(self):
        from backend.tasks.ingestion_tasks import run_job_discovery
        self._check_task(run_job_discovery)

    def test_email_tasks_bound(self):
        from backend.tasks.email_tasks import run_email_monitor
        self._check_task(run_email_monitor)

    def test_followup_tasks_bound(self):
        from backend.tasks.followup_tasks import run_followup_check
        self._check_task(run_followup_check)

    def test_digest_tasks_bound(self):
        from backend.tasks.digest_tasks import run_daily_digest
        self._check_task(run_daily_digest)

    def test_execution_tasks_bound(self):
        from backend.tasks.execution_tasks import (
            run_application_submission,
            run_status_tracking,
            run_email_outreach,
        )
        for task in [run_application_submission, run_status_tracking, run_email_outreach]:
            self._check_task(task)

    def test_composition_tasks_bound(self):
        from backend.tasks.composition_tasks import (
            run_resume_tailoring,
            run_cover_letter_generation,
        )
        for task in [run_resume_tailoring, run_cover_letter_generation]:
            self._check_task(task)

    def test_intelligence_tasks_bound(self):
        from backend.tasks.intelligence_tasks import (
            run_match_scoring,
            run_classification,
            run_qa_verification,
        )
        for task in [run_match_scoring, run_classification, run_qa_verification]:
            self._check_task(task)


class TestErrorHandlingModule:
    def test_task_error_hierarchy(self):
        from backend.tasks.error_handling import (
            TaskError,
            ProviderError,
            DatabaseError,
            ExternalServiceError,
        )
        assert issubclass(ProviderError, TaskError)
        assert issubclass(DatabaseError, TaskError)
        assert issubclass(ExternalServiceError, TaskError)
        assert issubclass(TaskError, Exception)

    def test_task_error_attributes(self):
        from backend.tasks.error_handling import TaskError
        err = TaskError("test msg", task_name="my_task", details={"k": "v"})
        assert err.message == "test msg"
        assert err.task_name == "my_task"
        assert err.details == {"k": "v"}
        assert str(err) == "test msg"

    def test_handle_task_errors_decorator_re_raises_task_error(self):
        from backend.tasks.error_handling import handle_task_errors, TaskError

        class FakeTask:
            name = "test_task"

        @handle_task_errors
        def my_func(self):
            raise TaskError("already a task error")

        with pytest.raises(TaskError, match="already a task error"):
            my_func(FakeTask())

    def test_handle_task_errors_decorator_wraps_generic_exception(self):
        from backend.tasks.error_handling import handle_task_errors, TaskError

        class FakeTask:
            name = "test_task"

        @handle_task_errors
        def my_func(self):
            raise ValueError("something broke")

        with pytest.raises(TaskError, match="something broke") as exc_info:
            my_func(FakeTask())
        assert exc_info.value.task_name == "test_task"


class TestRetryOnFailure:
    def test_simple_task_retries_on_exception(self):
        """Verify that run_job_discovery retries when the agent raises."""
        from backend.tasks.ingestion_tasks import run_job_discovery

        mock_self = MagicMock()
        mock_self.name = "backend.tasks.ingestion_tasks.run_job_discovery"
        mock_self.request.retries = 0
        mock_self.retry.side_effect = Exception("retry triggered")

        with patch(
            "backend.tasks.ingestion_tasks.api_source_agent"
        ) as mock_agent:
            mock_agent.process.side_effect = Exception("provider down")

            # Get the raw function via source inspection
            import inspect
            source = inspect.getsource(run_job_discovery.__wrapped__)
            assert "self.retry(exc=e" in source

    def test_simple_task_returns_error_when_retries_exhausted(self):
        """Verify that run_job_discovery returns error dict when MaxRetriesReachedError."""
        from backend.tasks.ingestion_tasks import run_job_discovery

        import inspect
        source = inspect.getsource(run_job_discovery.__wrapped__)
        assert "retries_exhausted" in source
        assert "MaxRetriesReachedError" in source

    def test_all_tasks_have_retry_in_source(self):
        """Verify all task functions contain retry logic."""
        from backend.tasks.ingestion_tasks import run_job_discovery
        from backend.tasks.email_tasks import run_email_monitor
        from backend.tasks.followup_tasks import run_followup_check
        from backend.tasks.digest_tasks import run_daily_digest
        from backend.tasks.execution_tasks import (
            run_application_submission,
            run_status_tracking,
            run_email_outreach,
        )
        from backend.tasks.composition_tasks import (
            run_resume_tailoring,
            run_cover_letter_generation,
        )
        from backend.tasks.intelligence_tasks import (
            run_match_scoring,
            run_classification,
            run_qa_verification,
        )

        tasks = [
            run_job_discovery, run_email_monitor, run_followup_check,
            run_daily_digest, run_application_submission, run_status_tracking,
            run_email_outreach, run_resume_tailoring, run_cover_letter_generation,
            run_match_scoring, run_classification, run_qa_verification,
        ]

        for task in tasks:
            import inspect
            source = inspect.getsource(task.__wrapped__)
            assert "self.retry" in source, f"{task.name} missing retry logic"
            assert "MaxRetriesReachedError" in source, f"{task.name} missing MaxRetriesReachedError handling"


class TestSchedulesDeleted:
    def test_schedules_module_removed(self):
        import importlib
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("backend.tasks.schedules")
