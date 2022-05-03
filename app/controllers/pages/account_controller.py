from flask import session, render_template
from flask_socketio import emit
from ... import socketio
from app.models.Users import users
from ... import db
from app.controllers.auth import auth_controller
from app.controllers.pages import pong_controller

def account():
    info = users.query.order_by(users.score.desc()).limit(8).all()

    # navbar:
    navbar = auth_controller.auth()

    data = users.query.filter_by(name = session['username']).first()


    if(data.win + data.lose == 0):
        win_rate = 0
    else:

        win_rate = data.win / (data.win + data.lose)
            
   

    content = render_template("pages/myaccount_page.html", data=data, win_rate=win_rate)
    
    foother = render_template("layout/foother.html")





    return render_template("template.html", title="Account", navbar=navbar, content=content, foother = foother)