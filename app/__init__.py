from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.models.Users import db


socketio = SocketIO()
db = SQLAlchemy()


def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__, template_folder='view')
    app.config.from_object('app.config')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    db.init_app(app)
    return app