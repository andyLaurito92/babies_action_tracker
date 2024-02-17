from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from configs import db

class Baby(db.Model):
    __tablename__ = 'babies'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    born_timestamp = db.Column(db.String(50), nullable=False)


class BabyRepository:
    def save_baby(self, baby):
        db.session.add(baby)
        db.session.commit()

    def get_all(self):
        return [{'first_name': baby.first_name, 'last_name': baby.last_name, 'born_timestamp': baby.born_timestamp} for baby in Baby.query.all()]
