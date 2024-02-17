from flask import Blueprint
from controllers.action_controller import index, add_action, get_all_actions, get_last_timestamps
from controllers.baby_controller import add_baby, get_all_babies

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/add_action', methods=['POST'])(add_action)
blueprint.route('/get_all_actions/<action>', methods=['GET'])(get_all_actions)
blueprint.route('/get_last_timestamps', methods=['GET'])(get_last_timestamps)

blueprint.route('/baby/add', methods=['POST'])(add_baby)
blueprint.route('/baby/get_all', methods=['GET'])(get_all_babies)
