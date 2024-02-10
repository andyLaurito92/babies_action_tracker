from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class BabyAction(db.Model):
    __tablename__ = 'baby_actions'

    id = db.Column(db.Integer, primary_key=True)
    action_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=True)

class BabyActionStatuses(db.Model):
    __tablename__ = 'baby_action_statuses'

    id = db.Column(db.Integer, primary_key=True)
    action_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)


class ActionRepository:
    def negate_status(self, status):
        if status == 'STARTED':
            return 'ENDED'
        else:
            return 'STARTED'

    def save_action(self, action, timestamp):
        action_status_record = BabyActionStatuses.query.filter_by(action_name=action).first()
        action_status_record.status = self.negate_status(action_status_record.status)
        db.session.add(BabyAction(action_name=action, timestamp=timestamp, status=action_status_record.status))
        db.session.commit()

    def get_all(self, action):
        return BabyAction.query.filter_by(action_name=action).all()

    def get_last_timestamp_for(self, action_name):
        result = db.session.query(BabyAction).from_statement(text(f"select * from baby_actions where action_name = '{action_name}' ORDER BY timestamp DESC limit 1;")).first()
        return result.timestamp if result != None else 'No entry yet'

    def get_latest_timestamps(self, actions):
        return [{'action': action_name,
                 'timestamp': self.get_last_timestamp_for(action_name)} for action_name in actions]

