# fichier de test

# actu : test les colisions

from math import *
from random import choice


"""
physique de pong :

quand la balle touche le mur alors sa fait un angle de 90°

lorsqu'elle touche la raquette, l'angle varie en fonction de zone de la raquette (au milieu = renvoie tout droit, et plus on dessent ou monte, plus l'angle est grand )

"""


class GameProcessus:

    """
    class pong:

        Gestion du jeu, collision de la balle sur les différentes surface, ...
        le code à été prévut initialement pour être en multi class (class : ball, area, player), mais manque de temps pour l'implémentation

        Input : 
            arearange (list): area of the game
            defaultSpeed (int): default speed of the ball 


    """

    def __init__(self, areaRange=[1000, 1000], defaultSpeed=10):
        self.areaRange = areaRange
        self.defaultSpeed = defaultSpeed

        """
        représentation des coordonnées des segments:

        ((x.left,x.right), (y.left,y.right))
        """

        # list of area dimension  :
        self.topArea = ((0, self.areaRange[0]),
                        (self.areaRange[1], self.areaRange[1]))
        self.bottomArea = ((0, self.areaRange[0]), (0, 0))
        self.leftArea = ((0, 0), (0, self.areaRange[1]))
        self.rightArea = (
            (self.areaRange[0], self.areaRange[0]), (self.areaRange[1], self.areaRange[1]))

        self.area = (self.topArea, self.bottomArea,
                     self.leftArea, self.rightArea)

        # initialisation of the ball
        # position ball (x,y), init : placé au milieu de la zone
        self.ballPos = [self.areaRange[0]/2, self.areaRange[1]/2]

        # vector of ball + speed ( [x,y,speed])
        self.ballVector = [choice([i for i in range(-8, 8) if i not in [0]]), choice(
            [i for i in range(-8, 8) if i not in [0]]), self.defaultSpeed]

        # initialization raquettes, racket dimension :( 10 x 100 ) :
        self.raquettePos = [[[50+0, 50+10], [0, 100]],
                            [[self.rightArea[0][0]-50-10, self.rightArea[0][0]-50], [0, 100]]]

        #(scorePlayer1, scorePlayer2)
        self.gameScore = [0, 0]

    # fonction qui détecte si la balle touche un mur de la zone
    def isWallTouched(self, newBallPosition):
        # check si position x de la balle est = a une position d'un bord ( si oui alors ie : elle le touche)

        # Hit top
        if(newBallPosition[1] >= self.topArea[1][0]):
            print("Hit top")
            self.ballVector[1] *= -1
            return True

        # Hit bottom
        elif(newBallPosition[1] <= self.bottomArea[1][0]):
            print("Hit bottom")
            self.ballVector[1] *= -1
            return True

        # Hit left = add point
        elif(newBallPosition[0] <= self.leftArea[0][0]):
            print("Hit left")
            self.ballVector[0] *= -1

            # le joueur 1 a marqué
            self.gameScore[0] += 1
            self.newRound()

            return True

        # Hit right = add point
        elif(newBallPosition[0] >= self.rightArea[0][0]):
            print("Hit right")
            self.ballVector[0] *= -1

            # le joueur 2 a marqué
            self.gameScore[1] += 1
            self.newRound()

            return True

        # No hit
        else:
            return False

    def isRaquetteTouched(self, newBallPosition):
        # on cherche a savoir si la balle touche la raquette
        # si oui, alors on calcule en fonction de point de touche le nouveau vecteur de la balle

        # parcours des deux raquettes des joueurs
        for player in range(2):

            # si la balle rentre dans la zone d'une raquettes
            if(self.raquettePos[player][0][1] >= newBallPosition[0] >= self.raquettePos[player][0][0] and self.raquettePos[player][1][1] >= newBallPosition[1] >= self.raquettePos[player][1][0]):

                # debug :
                print("raquette touché : ", player)
                print("ballposition : ", self.ballPos)
                print("ballVector : ", self.ballVector)
                print("raquette : ", self.raquettePos)

                print(self.raquettePos[player][0][0],
                      newBallPosition[0], self.raquettePos[player][0][1])
                print(self.raquettePos[player][1][1],
                      newBallPosition[1], self.raquettePos[player][1][0])

                # new vector after hit
                """
                this part of function have to role to determinate the new vector of the ball after hit the raquette of a player     
                """

                percentage = ((newBallPosition[1] - self.raquettePos[player][1][0]) / (
                    self.raquettePos[player][1][1] - self.raquettePos[player][1][0])) * 2

                print("percentage : ", percentage)
                print(newBallPosition[1], self.raquettePos[player][1][0],
                      self.raquettePos[player][1][1], self.raquettePos[player][1][0])

                if(percentage >= 0.8 and percentage <= 1.2):
                    self.ballVector[0] *= -1
                    self.ballVector[1] = 0

                elif(percentage > 1.2):
                    # limit of the ball angle
                    if(percentage > 1.6):
                        percentage = 1.6

                    self.ballVector[0] *= -1
                    self.ballVector[1] = percentage

                elif(percentage < 0.8):
                    # limit of the ball angle
                    if(percentage < 0.4):
                        percentage = 0.4

                    self.ballVector[0] *= -1
                    self.ballVector[1] = percentage

                # ajoiut de la vitesse
                self.ballVector[2] += 5

                return True

        return False

    # fonction qui calcule les nouvelles coordonné de la balle
    def newBallPosition(self):

        # speed = nombre de fois que le vecteur sera multiplié : ( speed = self.ballVector[2] )
        for i in range(self.ballVector[2]):
            # on normalise le vecteur ( srqr(x² + y²) )
            vectorNormalized = sqrt(
                self.ballVector[0]**2 + self.ballVector[1]**2)

            """
            Prochaine posi de la balle =

                position x actuelle + x du vecteur / par sa longeur
                position y actuelle + y du vecteur / par sa longeur
            
            """

            #print("speed : ", self.ballVector[2], i)
            #print("ballposition : ", self.ballPos)
            #print("ballVector : ", self.ballVector)
            #print("raquette : ", self.raquettePos)
            #print("vectorNormalized : ", vectorNormalized)
            #print('score : ', self.gameScore)

            tempoBallPosition = [self.ballPos[0] + self.ballVector[0] /
                                 vectorNormalized, self.ballPos[1] + self.ballVector[1] / vectorNormalized]

            # isWallTouched :
            if(self.isWallTouched(tempoBallPosition) == True):
                print("mur touché !")

            elif(self.isRaquetteTouched(tempoBallPosition) == True):
                print("raquette touché :")

            else:
                #print("continu son chemin")
                # la ball ne rentre pas en colision, elle continu son chemin
                self.ballPos = tempoBallPosition
                # return self.ballPos
        return self.ballPos

    def moveRaquette(self, player, action):

        # gestion des raquettes des deux joueurs
        # si -> pressé alors on check si le bas de la bar touche
        # si <- pressé alors on check si le haut de la bar touche
        # si ça touche pas alors on applique le mouvement a x1 et x2

        # si va vers le haut, check si le bas de la raquette touche
        if(action < 0 and self.raquettePos[player][1][0] + action < self.bottomArea[1][0]):
            # on colle la raquette au bas
            self.raquettePos[player][1][0] = self.bottomArea[1][0]
            # + taille de la raquette / à rajouter
            self.raquettePos[player][1][1] = self.raquettePos[player][1][0] + 100

        # si va vers le bas
        elif(action > 0 and self.raquettePos[player][1][1] + action > self.topArea[1][0]):
            self.raquettePos[player][1][1] = self.topArea[1][0]
            # - taille de la raquette / à rajouter
            self.raquettePos[player][1][0] = self.raquettePos[player][1][2] - 100

        # la raquette ne touchera pas, alors on applique l'action
        else:
            self.raquettePos[player][1][0] += action
            self.raquettePos[player][1][1] += action

    def newRound(self):
        # gestion des rounds et remise a 0 l'or d'un point marqué

        # remize a 0 de la balle
        self.ballVector = [choice([i for i in range(-8, 8) if i not in [0]]), choice(
            [i for i in range(-8, 8) if i not in [0]]), self.defaultSpeed]
        self.ballPos = [self.areaRange[0]/2, self.areaRange[1]/2]

        # actualisation des donnéees
        self.gameInfo()

        # debug
        # sleep(3)

    def gameInfo(self):
        # on envoie les infos info du jeu au client :
        # au lancement ou bien en cas de spectateur

        return {
            'ballPos': self.ballPos,
            'score': self.gameScore,
            'gameArea': self.area,
            'raquettes': self.raquettePos
        }


# Class Test
testPong = GameProcessus()


# Test collision with wall :
testNewBall1 = [50, 0]
testNewBall2 = [125, 500]
testNewBall3 = [500, 500]

assert(testPong.isWallTouched(testNewBall1) == True)
assert(testPong.isWallTouched(testNewBall2) == False)
assert(testPong.isWallTouched(testNewBall3) == False)

