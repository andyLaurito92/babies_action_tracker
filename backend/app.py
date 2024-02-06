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
@app.route('/get_all_actions/<action_type>', methods=['GET'])
def get_all_actions(action_type):
    actions = baby_action_repository.get_all(action_type)
    action_data = [
        {
            'action_type': action.action_type,
            'status': action.status,
            'timestamp': action.timestamp,
            'start_timestamp': action.start_timestamp,
            'food_type': action.food_type if hasattr(action, 'food_type') else None,
            'consistency': action.consistency if hasattr(action, 'consistency') else None,
            'wetness': action.wetness if hasattr(action, 'wetness') else None,
            'duration_minutes': action.duration_minutes if hasattr(action, 'duration_minutes') else None,
        }
        for action in actions
    ]
    return jsonify(action_data)

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
