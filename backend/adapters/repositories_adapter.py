from flask_sqlalchemy import SQLAlchemy
from ports.repositories import BabyActionRepository
from core.actions import EatAction, PoopAction, DiaperChangeAction, SleepAction

db = SQLAlchemy()

class EatActionModel(EatAction, db.Model):
    __tablename__ = 'eat_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    food_type = db.Column(db.String(50), nullable=True)

class EatActionStatus(db.Model):
    __tablename__ = 'eat_action_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    

class PoopActionModel(db.Model):
    __tablename__ = 'poop_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    consistency = db.Column(db.String(50), nullable=True)

class DiaperChangeActionModel(db.Model):
    __tablename__ = 'diaper_change_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    wetness = db.Column(db.String(50), nullable=True)

class SleepActionModel(db.Model):
    __tablename__ = 'sleep_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class SleepActionStatus(db.Model):
    __tablename__ = 'sleep_action_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    

class SQLiteBabyActionRepository(BabyActionRepository):
    def save(self, baby_action):
        db.session.add(baby_action)
        db.session.commit()

    def get_all(self, action_type):
        if action_type == 'eat':
            return [ EatAction(timestamp=model.timestamp, food_type=model.food_type, status=model.status) for model in EatActionModel.query.all() ]
        elif action_type == 'poop':
            return [ PoopAction(timestamp=model.timestamp, consistency=model.consistency) for model in PoopActionModel.query.all() ]
        elif action_type == 'diaper_change':
            return [ DiaperChangeAction(timestamp=model.timestamp, wetness=model.wetness) for model in DiaperChangeActionModel.query.all() ]
        elif action_type == 'sleep':
            return [ SleepAction(timestamp=model.timestamp, duration_minutes=model.duration_minutes, status=model.status) for model in SleepActionModel.query.all() ]
        else:
            raise ValueError('Invalid action type')

    def get_status_from(self, action_type):
        if action_type == 'eat':
            return EatActionStatus.query.one()
        elif action_type == 'sleep':
            return SleepActionStatus.query.one()
        
