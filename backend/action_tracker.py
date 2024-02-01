import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

actions = []

DIRECTORY = "/Users/andreslaurito/repos/babies_action_tracker/backend"
ACTIONS = ["sleep", "eat", "poop", "diaper_change"]

# create a logger
logger = logging.getLogger()

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

@app.route('/add_action', methods=['POST'])
def add_action():
    data = request.get_json()

    if 'action' not in data or 'timestamp' not in data:
        return jsonify({'error': 'Both action and timestamp parameters are required'}), 400
    elif data['action'] not in ACTIONS:
        return jsonify({'error': f"Action was {data['action']} which is not expected"}), 400

    action = {
        'action': data['action'],
        'timestamp': data['timestamp'],
    }

    actions.append(action)
    save_action_to_metrics_file(data['action'], data['timestamp'])

    return jsonify({'message': 'Action added successfully'}), 201

@app.route('/get_actions', methods=['GET'])
def get_actions():
    return jsonify(actions)


def append_to_file(filename, text):
    with open(filename, "a") as file:
        file.write(text)


def get_action_from(input_text):
    for action in ACTIONS:
        if action in input_text:
            return action

    # if we are here no action was detected, something went wrong!
    logger.error(f"No action was found in {input_text}")


def get_and_update_status_for(action):
    """ Naive function that negates the current status.
    If the status was STARTED, it returns ENDED and saves the status to the file
    corresponding to the action recieved. Otherwise it does the opposite."""
    action_status_file = f"{DIRECTORY}/data/{action}_status.txt"
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


def save_action_to_metrics_file(action, time_of_action):
    action_filename = f"{DIRECTORY}/data/{action}.csv"
    status = get_and_update_status_for(action)
    append_to_file(action_filename, f"{time_of_action}, {status} \n")
    logger.info(f"Text has been saved to {action_filename}")


if __name__ == "__main__":
    # This allows the Flask app to accept connections from any IP address on your local network
    app.run(host='0.0.0.0', port=5001)
