import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from datetime import datetime
from action_model import ActionRepository, db, EatActionStatus, SleepActionStatus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_actions.db'

DIRECTORY = "/Users/andreslaurito/repos/babies_action_tracker/backend"
ACTIONS = ("sleep", "eat", "poop", "diaper_change", "bath")

# create a logger
logger = logging.getLogger()

action_repo = ActionRepository()

# Configure a handler for all messages (INFO and above) to a general log file
file_handler_all = logging.FileHandler(f"{DIRECTORY}/logs/all_messages.log")
file_handler_all.setLevel(logging.INFO)
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

def is_valid_action(data):
    if 'timestamp' not in data:
        return False, jsonify({'error': 'Timestamp parameters is required'}), 400
    return True, {}

    
@app.route('/add_eat_action', methods=['POST'])
def add_eat_action():
    data = request.get_json()

    is_valid, message = is_valid_action(data)
    if not is_valid:
        return message
    
    #save_action_to_metrics_file(data['action'], data['timestamp'])
    action_repo.save_eat_action(data['timestamp'])

    return jsonify({'message': 'Action added successfully'}), 201

@app.route('/add_sleep_action', methods=['POST'])
def add_sleep_action():
    logger.info("Going to save new sleep action")
    data = request.get_json()

    is_valid, message = is_valid_action(data)
    if not is_valid:
        logger.info("Action recieved was not valid")
        return message
    
    #save_action_to_metrics_file(data['action'], data['timestamp'])
    logger.info("Saving in db")
    action_repo.save_sleep_action(data['timestamp'])
    logger.info("Saved successfully")

    return jsonify({'message': 'Action added successfully'}), 201

@app.route('/add_poop_action', methods=['POST'])
def add_poop_action():
    logger.info("Going to save new poop action")
    data = request.get_json()

    is_valid, message = is_valid_action(data)
    if not is_valid:
        return message
    
    #save_action_to_metrics_file(data['timestamp'])
    action_repo.save_poop_action(data['timestamp'])

    return jsonify({'message': 'Action added successfully'}), 201

@app.route('/add_diaper_change_action', methods=['POST'])
def add_diaper_change_action():
    data = request.get_json()

    is_valid, message = is_valid_action(data)
    if not is_valid:
        return message
    
    #save_action_to_metrics_file(data['action'], data['timestamp'])
    action_repo.save_diaper_change_action(data['timestamp'])

    return jsonify({'message': 'Action added successfully'}), 201

@app.route('/add_bath_action', methods=['POST'])
def add_bath_action():
    data = request.get_json()

    is_valid, message = is_valid_action(data)
    if not is_valid:
        return message
    
    #save_action_to_metrics_file(data['action'], data['timestamp'])
    action_repo.save_bath_action(data['timestamp'])

    return jsonify({'message': 'Action added successfully'}), 201


@app.route('/get_bath_actions', methods=['GET'])
def get_bath_actions():
    return jsonify([(bath_action.timestamp, bath_action.status) for bath_action in action_repo.get_all_bath_actions()])


@app.route('/get_eat_actions', methods=['GET'])
def get_eat_actions():
    return jsonify([(eat_action.timestamp, eat_action.status) for eat_action in action_repo.get_all_eat_actions()])

@app.route('/get_eat_action_status', methods=['GET'])
def get_eat_action_status():
    return action_repo.get_eat_action_status().status

@app.route('/get_sleep_actions', methods=['GET'])
def get_sleep_actions():
    return jsonify([(sleep_action.timestamp, sleep_action.status) for sleep_action in action_repo.get_all_sleep_actions()])

@app.route('/get_sleep_action_status', methods=['GET'])
def get_sleep_action_status():
    return action_repo.get_sleep_action_status().status

@app.route('/get_diaper_change_actions', methods=['GET'])
def get_diaper_change_actions():
    return jsonify([diaper_change_action.timestamp for diaper_change_action in action_repo.get_all_diaper_change_actions()])

@app.route('/get_poop_actions', methods=['GET'])
def get_poop_actions():
    return jsonify([poop_action.timestamp for poop_action in action_repo.get_all_poop_actions()])


if __name__ == "__main__":
    # This allows the Flask app to accept connections from any IP address on your local network
    logger.info("Initializing app")
    db.init_app(app)
    with app.app_context():
        db.create_all()
        logger.info("Initializing statuses of sleep & eat actions")
        if EatActionStatus.query.count() == 0:
            db.session.add(EatActionStatus(status='ENDED'))
            db.session.commit()
        if SleepActionStatus.query.count() == 0:
            db.session.add(SleepActionStatus(status='ENDED'))
            db.session.commit()
        
    app.run(host='0.0.0.0', port=5001)
