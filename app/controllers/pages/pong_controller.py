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

        # envoie l'état du nombre de pret

        socketio.emit(
            'statuGame', {'player1': player1['username'], "player2": player2['username']})

        if(gameStatu == True):
            socketio.emit('display', data=True)

        # cas de deux joueurs qui sont prets -> lancement du jeu
        if(player1['username'] != "" and player2['username'] != "" and gameStatu == False):
            gameStatu = True
            print("jeu tourné sur on")

            # change display ( gif pong -> real pong)

            socketio.emit('display', data=True)

            socketio.sleep(0.5)
            game()

    # envoie l'état du jeu lors du chargement de la page
    @socketio.on('connexion_serveur')
    def connexion_serveur():
        playerInfo()

    # gestion du joueur 1 isReady

    @socketio.on('readyPlayer')
    def isReadyPlayer1():
        global player1
        global player2

        # check si utulisateur connecté
        if session.get("username"):
            # check si place libre
            if(player1['username'] == '' or player2['username'] == ''):
                # check si place vide et check doublon
                if(player1['username'] != session.get("username") and player2['username'] != session.get("username")):

                    # attribu une place au joueur
                    if(player1['username'] == ''):
                        player1['username'] = session.get("username")
                    else:
                        player2['username'] = session.get("username")

                    # on actualise les données de statu
                    playerInfo()

    def game():

        # Game started
        party = GameProcessus([680, 540])

        fps_limiter = LimitFPS(fps=30)
        fps_counter = FPSCounter()

        global gameStatu
        global player1
        global player2

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

                # check win
                if(data['score'][0] == 8 or data['score'][1] == 8):

                    updateJ1 = db.session.query(users).filter_by(name=player1['username']).first()
                    updateJ2 = db.session.query(users).filter_by(name=player2['username']).first()


                    if(data['score'][0] == 8):

                        winner = player2['username']
                        loosing = player1['username']
                        score = [data['score'][0], data['score'][1]]
                        updateJ2.win += 1
                        updateJ1.lose += 1
 

                    else:


                        winner = player1['username']
                        loosing = player2['username']
                        score = [data['score'][1], data['score'][0]]
                        updateJ1.win += 1
                        updateJ2.lose += 1


                    updateJ1.score += data['score'][1]
                    updateJ1.nb_partie += 1
                    db.session.add(updateJ1)
                    db.session.commit()

                    updateJ2.score += data['score'][0]
                    updateJ2.nb_partie += 1
                    db.session.add(updateJ2)
                    db.session.commit()
                    
                    # envoie du message aux joueurs et spectateur
                    socketio.emit('PlayerWin', {'winner': winner, "loosing": loosing, 'score': score})
                    socketio.emit('display', data=False)
                    socketio.sleep(0.01)

                    # reset du jeu
                    gameStatu=False
                    player1['username'] = ''
                    player2['username'] = ''
                    playerInfo()



                



