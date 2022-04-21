from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name