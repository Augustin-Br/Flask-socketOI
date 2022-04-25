from flask import session, render_template
from flask_socketio import emit
from ... import socketio
from app.models.Users import users
from ... import db
from app.controllers.auth import auth_controller
from app.controllers.pages import pong_controller

def account():
    
    # navbar:
    navbar = auth_controller.auth()

    content = render_template("pages/myaccount_page.html")
    
    foother = render_template("layout/foother.html")

    return render_template("template.html", title="Account", navbar=navbar, content=content, foother = foother)