from flask import session, render_template
from app.models.Users import users
from ... import socketio
from ... import db

from app.controllers.gameManagement import GameProcessus
from fps_limiter import LimitFPS, FPSCounter

player1 = {'username': ''}
player2 = {'username': ''}
gameStatu = False

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

            socketio.sleep(0.5)
            game()

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
                
    return render_template('pages/pong_page.html')
