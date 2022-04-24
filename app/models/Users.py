from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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

def encrypt_password(password):
    
    return generate_password_hash(password)


def password_verif(password, db_password):  
    
    hashed_value = generate_password_hash(password)
    
    stored_password = db_password
    
    result = check_password_hash(stored_password, password)
    
    return str(result)
   