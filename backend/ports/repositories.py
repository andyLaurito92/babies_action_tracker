from abc import ABC, abstractmethod
from core.actions import BabyAction

class BabyActionRepository(ABC):
    @abstractmethod
    def save(self, baby_action):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_status_from(self, action_type):
        pass
        
