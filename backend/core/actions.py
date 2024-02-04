class BabyAction:
    DIRECTORY = "/Users/andreslaurito/repos/babies_action_tracker/backend"

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def get_and_update_status_for(self, action_type):
        """ Naive function that negates the current status.
        If the status was STARTED, it returns ENDED and saves the status to the file
        corresponding to the action recieved. Otherwise it does the opposite."""
        action_status_file = f"{self.DIRECTORY}/data/{action_type}_status.txt"
        current_action_status = ""
        next_action_status = ""
        with open(action_status_file, "r") as action_status_content:
            current_action_status = action_status_content.read()
            if current_action_status == "STARTED":
                next_action_status = "ENDED"
            else:
                next_action_status = "STARTED"
                
        with open(action_status_file, "w") as action_status_content:
            action_status_content.write(next_action_status)
                    
        return next_action_status

    @classmethod
    def build(cls, action_type, timestamp, data):
        if action_type == 'eat':
            return EatAction(timestamp, data.get('food_type'))
        elif action_type == 'poop':
            return PoopAction(timestamp, data.get('consistency'))
        elif action_type == 'diaper_change':
            return DiaperChangeAction(timestamp, data.get('wetness'))
        elif action_type == 'sleep':
            return SleepAction(timestamp)
        else:
            raise Exception(f"Unexpected action type: {action_type}")


class EatAction(BabyAction):
    def __init__(self, timestamp, food_type):
        super().__init__(timestamp)
        self.status = self.get_and_update_status_for('eat')
        self.food_type = food_type

class PoopAction(BabyAction):
    def __init__(self, timestamp, consistency):
        super().__init__(timestamp)
        self.consistency = consistency

class DiaperChangeAction(BabyAction):
    def __init__(self, timestamp, wetness):
        super().__init__(timestamp)
        self.wetness = wetness

class SleepAction(BabyAction):
    def __init__(self, timestamp, duration_minutes):
        super().__init__(timestamp)
        self.status = self.get_and_update_status_for('sleep')
