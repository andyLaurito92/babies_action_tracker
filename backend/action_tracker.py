import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from action_model import ActionRepository, db, BabyAction, BabyActionStatuses

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_actions.db'

DIRECTORY = "/Users/andreslaurito/repos/babies_action_tracker/backend"
ACTIONS = ("sleep", "eat", "poop", "diaper_change", "bath", "washing_diapers")

# create a logger
logger = logging.getLogger()

action_repo = ActionRepository()

# Configure a handler for all messages (INFO and above) to a general log file
file_handler_all = logging.FileHandler(f"{DIRECTORY}/logs/all_messages.log")
file_handler_all.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_all.setFormatter(file_formatter)

# Configure a handler for error messages only to a separate log file
file_handler_error = logging.FileHandler(f"{DIRECTORY}/logs/error.log")
file_handler_error.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_error.setFormatter(error_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler_all)
logger.addHandler(file_handler_error)

@app.route('/')
def index():
   return render_template('action_buttons.html')

@app.route('/add_action', methods=['POST'])
def add_action():
    match request.get_json():
        case {"action": val_action, "timestamp": val_timestamp}:
            logger.info(f"Request is valid. Values {val_action} {val_timestamp}")
            action_repo.save_action(val_action, val_timestamp)
            return jsonify({'message': 'Action added successfully'}), 201
        case _:
            logger.info(f"Request is invalid")
            return jsonify({'message': 'Request is invalid. Please provide both action and timestamp'}), 400    

@app.route('/get_all_actions/<action>', methods=['GET'])
def get_all_actions(action):
    res = action_repo.get_all(action)
    return jsonify([(baby_action.action_name, baby_action.timestamp, baby_action.status) for baby_action in res])

@app.route('/get_last_timestamps', methods=['GET'])
def get_last_timestamps():
    return jsonify({'timestamps': action_repo.get_latest_timestamps(ACTIONS)})

if __name__ == "__main__":
    # This allows the Flask app to accept connections from any IP address on your local network
    logger.info("Initializing app")
    db.init_app(app)
    with app.app_context():
        db.create_all()
        logger.info("Initializing statuses of all actions")
        if BabyActionStatuses.query.count() == 0:
            for action in ACTIONS:
                db.session.add(BabyActionStatuses(action_name=action, status='ENDED'))
            db.session.commit()
       
    app.run(host='0.0.0.0', port=5001)
