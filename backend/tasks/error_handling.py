import logging
import functools
from typing import Callable, Any

logger = logging.getLogger(__name__)


class TaskError(Exception):
    """Base exception for task errors."""
    def __init__(self, message: str, task_name: str = None, details: dict = None):
        self.message = message
        self.task_name = task_name
        self.details = details or {}
        super().__init__(self.message)


class ProviderError(TaskError):
    """AI provider failed."""
    pass


class DatabaseError(TaskError):
    """Database operation failed."""
    pass


class ExternalServiceError(TaskError):
    """External service (email, ATS) failed."""
    pass


def handle_task_errors(task_func: Callable) -> Callable:
    """Decorator to wrap task functions with proper error handling."""
    @functools.wraps(task_func)
    def wrapper(self, *args, **kwargs):
        task_name = self.name
        try:
            return task_func(self, *args, **kwargs)
        except TaskError:
            raise
        except Exception as e:
            logger.error(f"Task {task_name} failed with unexpected error: {e}", exc_info=True)
            raise TaskError(
                message=str(e),
                task_name=task_name,
                details={"args": str(args), "kwargs": str(kwargs)}
            )
    return wrapper
