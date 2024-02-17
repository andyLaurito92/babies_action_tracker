import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DIRECTORY = "/Users/andreslaurito/repos/babies_action_tracker/backend"

# create a logger
logger = logging.getLogger()

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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DIRECTORY}/instance/baby_actions.db"

db = SQLAlchemy()

