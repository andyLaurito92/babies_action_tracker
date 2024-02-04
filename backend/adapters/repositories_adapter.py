from flask_sqlalchemy import SQLAlchemy
from ports.repositories import BabyActionRepository
from core.actions import EatAction, PoopAction, DiaperChangeAction, SleepAction

db = SQLAlchemy()

class EatActionModel(EatAction, db.Model):
    __tablename__ = 'eat_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    food_type = db.Column(db.String(50), nullable=True)

class PoopActionModel(PoopAction, db.Model):
    __tablename__ = 'poop_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    consistency = db.Column(db.String(50), nullable=True)

class DiaperChangeActionModel(DiaperChangeAction, db.Model):
    __tablename__ = 'diaper_change_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    wetness = db.Column(db.String(50), nullable=True)

class SleepActionModel(SleepAction, db.Model):
    __tablename__ = 'sleep_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class SQLiteBabyActionRepository(BabyActionRepository):
    def save(self, baby_action):
        db.session.add(baby_action)
        db.session.commit()

    def get_all(self, action_type):
        if action_type == 'eat':
            return EatActionModel.query.all()
        elif action_type == 'poop':
            return PoopActionModel.query.all()
        elif action_type == 'diaper_change':
            return DiaperChangeActionModel.query.all()
        elif action_type == 'sleep':
            return SleepActionModel.query.all()
        else:
            raise ValueError('Invalid action type')
