from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    nb_partie = db.Column(db.Integer)
    score = db.Column(db.Integer)
    data_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, password, nb_partie, score):
        self.name = name
        self.password = password
        self.nb_partie = nb_partie
        self.score = score
        
   