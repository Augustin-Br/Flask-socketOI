from datetime import datetime
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

__author__ = "Brian Perret"

#Initialization and configuration of app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['DEBUG'] = True
app.config["SESSION_PERMANENT"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

#app.config['SQLALCHIMY_TRACK_MODIFICATIONS'] = False

#start session
Session(app)

#start socketio
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#start db
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    data_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name

#debbug
print("start")

#home page 
@app.route('/')
def index():
    return render_template('index.html')

"""
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    socketio.emit('test_socket',{'number': 'Youpie !'})
"""

#received messages :
@socketio.on('message_send')
def message_recu(data):
    print('received message: ' + str(data))
    message_to_send(data)

    


#send messages

def message_to_send(data):

    #check empty message
    if(data != '' and data != ' '):

        #user not login  -> anonymous
        if not session.get("username"):

            socketio.emit('message_to_send', {"user" : "anonymous", 'msg' : data})
        else:
            socketio.emit('message_to_send', {"user" : session.get("username"), 'msg' : data})


#login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    #user haven't session 
    if not session.get("username"):
        
        print("l'utilisateur n'a pas de session")

        #user login request 
        if(request.method=='POST'):
             #received login data
            print("l'utilisateur envoie les données d'authentification")

            username = request.form['username']

            #stock data into user's session

            session['username'] = username

            print("user name : ", session.get("username"))

            #redirection user to home page

            return redirect("/")

        else:
            print("l'utilisateur veux se connecté")
            return render_template('sign_in_page.html')

    else:
        #user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")

@app.route("/sign-up",  methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        
        #received login data
        print("l'utilisateur envoie les données d'inscription")

        #recup les données recus
        username = request.form['username']

        #check username already existe:
        user_found = users.query.filter_by(name=username).first()     

        if(user_found):
            print("nom déjà utilisé")
            socketio.emit('error', {'msg' : "username already exist"})
            return 

        else:
            data = users(username)
            db.session.add(data)
            db.session.commit()
            print("ok nom")
            return redirect('/')




        

    else:
        #l'utilisateur veux accèdé a la page d'inscription
        return render_template('sign_up_page.html')


@app.route("/sign-out")
def logout():
    session["username"] = None
    return redirect("/")


#database view
@app.route('/view_db')
def view_db():
    info = users.query.all()
    #print("info :",info)

    

    return render_template("view_db.html", data = info)

@socketio.on('yMousePos')
def yMousePos_recu(data):
    print('yMousePos: ' + str(data))
    socketio.emit('recuYMousePos', {'yMousePos' : data})


#socketio.emit('message_to_send', {"user" : "anonymous", 'msg' : data})

if __name__ == '__main__':
    db.create_all()

    socketio.run(app, host='127.0.0.1', port=1664)