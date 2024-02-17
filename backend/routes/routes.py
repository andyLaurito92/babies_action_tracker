from flask import Blueprint
from controllers.action_controller import index, add_action, get_all_actions, get_last_timestamps

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/add_action', methods=['POST'])(add_action)
blueprint.route('/get_all_actions/<action>', methods=['GET'])(get_all_actions)
blueprint.route('/get_last_timestamps', methods=['GET'])(get_last_timestamps)


