from flask import render_template
from flask_socketio import emit
from app.models.Users import users
from ... import db
from ... import socketio

def test():
    info = users.query.all()
    print("info :",info)
    return render_template("pages/view_db.html", data=info)

@socketio.on('yMousePos')
def yMousePos_recu(data):
    print('yMousePos: ' + str(data))
    socketio.emit('recuYMousePos', {'yMousePos': data})