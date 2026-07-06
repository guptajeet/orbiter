from abc import ABC, abstractmethod

class SubmissionResult:
    def __init__(self, status: str, message: str = "", application_id: str = None):
        self.status = status
        self.message = message
        self.application_id = application_id

class BaseATSAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def submit_application(self, application_data: dict, resume: str, cover_letter: str) -> SubmissionResult:
        pass

    @abstractmethod
    def check_status(self, application_id: str) -> str:
        pass

    @abstractmethod
    def get_supported_features(self) -> list[str]:
        pass
