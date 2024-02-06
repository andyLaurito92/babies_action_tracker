from ports.api import BabyActionAPI
from core.actions import BabyAction

class FlaskBabyActionAPI(BabyActionAPI):
    def __init__(self, action_repository):
        self.action_repository = action_repository

    def record_action(self, action_type, timestamp, data):
        baby_action = BabyAction.build(action_type, timestamp, data, self.action_repository)
        self.action_repository.save(action_type, timestamp, data)
