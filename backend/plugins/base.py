from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

class BaseSourcePlugin(BasePlugin):
    @abstractmethod
    def search_jobs(self, filters: dict) -> list:
        pass
        
    @abstractmethod
    def get_job_details(self, job_id: str) -> dict:
        pass

class BaseProviderPlugin(BasePlugin):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> dict:
        pass
        
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        pass

class BaseChannelPlugin(BasePlugin):
    @abstractmethod
    def send_message(self, contact: dict, message: dict) -> dict:
        pass
        
    @abstractmethod
    def check_responses(self) -> list:
        pass
