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
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)

    def __init__(self, name, password, nb_partie, score, win, lose):
        self.name = name
        self.password = password
        self.nb_partie = nb_partie
        self.score = score
        self.win = win
        self.lose = lose

def encrypt_password(password):
    
    return generate_password_hash(password)


def password_verif(password, db_password):  
    
    hashed_value = generate_password_hash(password)
    
    stored_password = db_password
    
    result = check_password_hash(stored_password, password)
    
    return str(result)

assert password_verif('password', encrypt_password('password')) == 'True' #test normal
assert password_verif('passworde', encrypt_password('password')) == 'False' #test mauvais mot de passe
assert password_verif('password', encrypt_password('passworde')) == 'False' #test mauvais mot de passe
assert password_verif('&(-_çàé', encrypt_password('&(-_çàé')) == 'True' #test normal avec caractère spéciaux
assert password_verif('&çàé', encrypt_password('&(-_çàé')) == 'False' #test mauvais mot de passe avec caractère spéciaux
assert password_verif('0123456789', encrypt_password('0123456789')) == 'True' #test normal avec nombre uniquement
assert password_verif('016789', encrypt_password('0123456789')) == 'False' #test mauvais mot de passe avec nombre uniquement
assert password_verif('0123456789', encrypt_password('016789')) == 'False' #test mauvais mot de passe avec nombre uniquement
assert password_verif('016789azerty&', encrypt_password('0123456789azerty&')) == 'False' #test mauvais mot de passe avec nombre et caractère
assert password_verif('0123456789azerty', encrypt_password('0123456789azerty')) == 'True' #test normal avec nombre et caractères