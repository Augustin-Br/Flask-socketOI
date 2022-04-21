from turtle import title
from flask import session, render_template
from flask_socketio import emit
from ... import socketio
from app.models.Users import users
from ... import db

def index():

    @socketio.on('message_send')
    def message_recu(data):
        print('received message: ' + str(data))
        message_to_send(data)


    # send messages
    def message_to_send(data):

        # check empty message
        if(data != '' and data != ' '):

            # user not login  -> anonymous
            if not session.get("username"):

                socketio.emit('message_to_send', {
                            "user": "anonymous", 'msg': data})
            else:
                socketio.emit('message_to_send', {
                            "user": session.get("username"), 'msg': data})

            
                


    return render_template('pages/index.html')

def home():
    info = users.query.all()

    #navbar:
    navbar = render_template("layout/navbar.html")


    content = render_template("pages/home.html", data = info)




    return render_template("template.html", title="Accueil", navbar = navbar, content = content)
