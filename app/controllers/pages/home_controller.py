from flask import session, render_template
from flask_socketio import emit
from ... import socketio
from app.models.Users import users
from ... import db
from app.controllers.auth import auth_controller
from app.controllers.pages import pong_controller

def home():
    info = users.query.order_by(users.score.desc()).limit(8).all()

    # navbar:
    navbar = auth_controller.auth()

    pong_controller.pong()

    content = render_template("pages/home_page.html", data=info)
    
    foother = render_template("layout/foother.html")

    return render_template("template.html", title="Accueil", navbar=navbar, content=content, foother = foother)
