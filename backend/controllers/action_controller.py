from flask import request, jsonify, render_template
from models.action_model import ActionRepository, BabyAction, BabyActionStatuses
from configs import logger

ACTIONS = ("sleep", "eat", "poop", "diaper_change", "bath", "washing_diapers")
action_repo = ActionRepository()

def initialize_action_controller():
   logger.info("Initializing statuses of all actions")
   for action in ACTIONS:
      if BabyActionStatuses.query.filter_by(action_name=action).count() == 0:
         db.session.add(BabyActionStatuses(action_name=action, status='ENDED'))
         db.session.commit()
            
def index():
   return render_template('action_buttons.html')

def add_action():
   match request.get_json():
      case {"action": val_action, "timestamp": val_timestamp}:
         logger.info(f"Request is valid. Values {val_action} {val_timestamp}")
         action_repo.save_action(val_action, val_timestamp)
         return jsonify({'message': 'Action added successfully'}), 201
      case _:
         logger.info(f"Request is invalid")
         return jsonify({'message': 'Request is invalid. Please provide both action and timestamp'}), 400    
      
def get_all_actions(action):
   res = action_repo.get_all(action)
   return jsonify([(baby_action.action_name, baby_action.timestamp, baby_action.status) for baby_action in res])

def get_last_timestamps():
   return jsonify({'timestamps': action_repo.get_latest_timestamps(ACTIONS)})

