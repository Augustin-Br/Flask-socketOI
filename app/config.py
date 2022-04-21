from datetime import timedelta

SECRET_KEY = 'secret!'
SESSION_TYPE = 'filesystem'
DEBUG = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=360)
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3'