from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from gameManagement import GameProcessus
from fps_limiter import LimitFPS, FPSCounter


__author__ = "Brian Perret"

# Initialization and configuration of app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['DEBUG'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=360)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

#app.config['SQLALCHIMY_TRACK_MODIFICATIONS'] = False

# start session
Session(app)

# start socketio
socketio = SocketIO(app, async_mode=None, logger=False, engineio_logger=False)

# start db
db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name


# debbug
print("start")

# home page


@app.route('/')
def index():
    return render_template('index.html')


"""
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    socketio.emit('test_socket',{'number': 'Youpie !'})
"""

# received messages :


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


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # user haven't session
    if not session.get("username"):

        print("l'utilisateur n'a pas de session")

        # user login request
        if(request.method == 'POST'):
            # received login data
            print("l'utilisateur envoie les données d'authentification")

            username = request.form['username']

            # stock data into user's session

            session['username'] = username

            print("user name : ", session.get("username"))

            # redirection user to home page

            return redirect("/")

        else:
            print("l'utilisateur veux se connecté")
            return render_template('sign_in_page.html')

    else:
        # user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")


@app.route("/sign-up",  methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':

        # received login data
        print("l'utilisateur envoie les données d'inscription")

        # recup les données recus
        username = request.form['username']

        # check username already existe:
        user_found = users.query.filter_by(name=username).first()

        if(user_found):
            print("nom déjà utilisé")
            socketio.emit('error', {'msg': "username already exist"})
            return

        else:
            data = users(username)
            db.session.add(data)
            db.session.commit()
            print("ok nom")
            return redirect('/')

    else:
        # l'utilisateur veux accèdé a la page d'inscription
        return render_template('sign_up_page.html')


@app.route("/sign-out")
def logout():
    session["username"] = None
    return redirect("/")


# database view ( test )
@app.route('/view_db')
def view_db():
    info = users.query.all()
    #print("info :",info)
    return render_template("view_db.html", data=info)


@socketio.on('yMousePos')
def yMousePos_recu(data):
    print('yMousePos: ' + str(data))
    socketio.emit('recuYMousePos', {'yMousePos': data})

# info sur les player, il faudra les initialisé lorsque que l'on cliquera sur start ou autre
# mais pour l'instant on initialise lors du démarage du serv


player1 = {'username': ''}
player2 = {'username': ''}
gameStatu = False


@app.route('/pong')
def pong():

    def playerInfo():
        """
        fonction qui permet de renseigner le nombre et nom des joueurs pret a joué


        2 places uniquement accessible pour des connectés

        les joueurs qui ne clique pas sur 'pret' son spectateur

        """
        global gameStatu

        # on recup les infos des player du serveur
        #global player1
        #global player2
        #global gameStatu

        # envoie l'état du nombre de pret
        socketio.emit(
            'statuGame', {'player1Info': player1, "player2Info": player2})

        # cas de deux joueurs qui sont prets -> lancement du jeu
        if(player1['username'] != "" and player2['username'] != "" and gameStatu == False):
            gameStatu = True
            print("jeu tourné sur on")

            socketio.sleep(1)
            game()

        """
        #probleme quand y'a un spec -> stop le jeu
        else:
            print(player1['username'], player2['username'], gameStatu)
            gameStatu = False
            print("jeu tourné sur off")
        """

    # envoie l'état du jeu lors du chargement de la page
    @socketio.on('connexion_serveur')
    def connexion_serveur():
        playerInfo()

    # gestion du joueur 1 isReady
    @socketio.on('readyPlayer1')
    def isReadyPlayer1():
        global player1
        global player2

        # check si utulisateur connecté
        if session.get("username"):
            # check si place vide et check doublon
            if(player2['username'] != session.get("username") and player1['username'] == ""):

                # on save le pseudo du joueur 1
                player1['username'] = session.get("username")

                # on actualise les données de statu
                playerInfo()

    # gestion du joueur 2 isReady

    @socketio.on('readyPlayer2')
    def isReadyPlayer2():
        global player1
        global player2

        # check si utulisateur connecté
        if session.get("username"):
            # check si place vide et check doublon
            if(player1['username'] != session.get("username") and player2['username'] == ""):

                # on save le pseudo du joueur 2
                player2['username'] = session.get("username")

                # on actualise les données de statu
                playerInfo()

    def game():
        #socketio.emit('statuGame', {'player1Info': player1, "player2Info" : player2})

        # Game started
        party = GameProcessus([500, 500])

        fps_limiter = LimitFPS(fps=30)
        fps_counter = FPSCounter()

        print('gameStatu : ', gameStatu)

        # cadenser le jeu a un certain nombre fixe de fps
        while (gameStatu):
            if fps_limiter():

                # recup les actions des joueurs

                @socketio.on('ArrowLeft')
                def raquetteAction():
                    if(session.get("username") == player1['username']):
                        party.moveRaquette(0, -50)
                    elif(session.get("username") == player2['username']):
                        party.moveRaquette(1, -50)

                @socketio.on('ArrowRight')
                def raquetteAction():
                    if(session.get("username") == player1['username']):
                        party.moveRaquette(0, 50)
                    elif(session.get("username") == player2['username']):
                        party.moveRaquette(1, 50)

                # debug :
                party.newBallPosition()

                # on recup les infos du jeu
                data = party.gameInfo()

                socketio.emit('gameInfo',  data)
                socketio.sleep(0.01)

                #ballPos = party.newBallPosition()
                #socketio.emit('gameInfo', {'ballPos' : ballPos})

                #print("current fps: %s" % fps_counter())

    return render_template('pong_test.html')

#socketio.emit('message_to_send', {"user" : "anonymous", 'msg' : data})


if __name__ == '__main__':
    db.create_all()

    socketio.run(app, host='127.0.0.1', port=1664)
