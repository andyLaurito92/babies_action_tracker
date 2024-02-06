from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class EatActionModel(db.Model):
    __tablename__ = 'eat_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class EatActionStatus(db.Model):
    __tablename__ = 'eat_action_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

class PoopActionModel(db.Model):
    __tablename__ = 'poop_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)

class BathActionModel(db.Model):
    __tablename__ = 'bath_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)


class DiaperChangeActionModel(db.Model):
    __tablename__ = 'diaper_change_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)


class SleepActionModel(db.Model):
    __tablename__ = 'sleep_actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class SleepActionStatus(db.Model):
    __tablename__ = 'sleep_action_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)


class ActionRepository:
    def negate_status(self, status):
        if status == 'STARTED':
            return 'ENDED'
        else:
            return 'STARTED'

    def save_eat_action(self, timestamp):
        eat_status_record = EatActionStatus.query.first()
        eat_status_record.status = self.negate_status(eat_status_record.status)
        db.session.add(EatActionModel(timestamp=timestamp, status=eat_status_record.status))
        db.session.commit()

    def save_sleep_action(self, timestamp):
        sleep_status_record = EatActionStatus.query.first()
        sleep_status_record.status = self.negate_status(sleep_status_record.status)
        db.session.add(SleepActionModel(timestamp=timestamp, status=sleep_status_record.status))
        db.session.commit()

    def save_diaper_change_action(self, timestamp):
        db.session.add(DiaperChangeActionModel(timestamp=timestamp))
        db.session.commit()

    def save_poop_action(self, timestamp):
        db.session.add(PoopActionModel(timestamp=timestamp))
        db.session.commit()

    def save_bath_action(self, timestamp):
        db.session.add(BathActionModel(timestamp=timestamp))
        db.session.commit()


    def get_all_eat_actions(self):
        return EatActionModel.query.all()

    def get_all_bath_actions(self):
        return BathActionModel.query.all()

    def get_eat_action_status(self):
        return EatActionStatus.query.first()

    def get_all_sleep_actions(self):
        return SleepActionModel.query.all()

    def get_all_diaper_change_actions(self):
        return DiaperChangeActionModel.query.all()

    def get_all_poop_actions(self):
        return PoopActionModel.query.all()



