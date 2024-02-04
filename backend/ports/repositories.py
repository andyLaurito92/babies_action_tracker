from abc import ABC, abstractmethod
from core.actions import BabyAction

class BabyActionRepository(ABC):
    @abstractmethod
    def save(self, baby_action: BabyAction):
        pass

    @abstractmethod
    def get_all(self):
        pass
