from flask import Flask, jsonify, request
from adapters.api_adapter import FlaskBabyActionAPI
from adapters.repositories_adapter import SQLiteBabyActionRepository, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_actions.db'
db.init_app(app)

# Initialize the adapters
baby_action_repository = SQLiteBabyActionRepository()
baby_action_api = FlaskBabyActionAPI(baby_action_repository)

# API endpoint to record baby actions
@app.route('/add_action', methods=['POST'])
def record_action():
    data = request.get_json()
    action_type = data.get('action')
    timestamp = data.get('timestamp')

    if not action_type or not timestamp:
        return jsonify({'error': 'Invalid request'}), 400

    baby_action_api.record_action(action_type, timestamp, data)
    return jsonify({'message': 'Action recorded successfully'}), 200

# API endpoint to get all recorded actions
@app.route('/get_all_actions', methods=['GET'])
def get_all_actions():
    actions = baby_action_repository.get_all()
    action_data = [{'action_type': action.action_type, 'timestamp': action.timestamp} for action in actions]
    return jsonify(action_data)

if __name__ == '__main__':
    app.run(debug=True)
