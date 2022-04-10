# fichier de test

# actu : test les colisions

from math import *
from fps_limiter import LimitFPS, FPSCounter



"""
physique de pong :

quand la balle touche le mur alors sa fait un angle de 90°

lorsqu'elle touche la raquette, l'angle varie en fonction de zone de la raquette (au milieu = renvoie tout droit, et plus on dessent ou monte, plus l'angle est grand )


"""


class GameProcessus:
    def __init__(self, areaRange=[1000, 1000], defaultSpeed=50):
        self.areaRange = areaRange
        self.defaultSpeed = defaultSpeed

        """
        représentation des coordonnées des segments:

        ((x.left,x.right), (y.left,y.right))
        """

        # liste index :
        self.topArea = ((0, self.areaRange[0]),(self.areaRange[1], self.areaRange[1]))
        self.bottomArea = ((0, self.areaRange[0]), (0, 0))
        self.leftArea = ((0, 0), (0, self.areaRange[1]))
        self.rightArea = ((self.areaRange[0], self.areaRange[0]), (self.areaRange[1], self.areaRange[1]))

        #self.area = [self.topArea, self.bottomArea, self.leftArea, self.rightArea]

        # initialisation de la ball

        # position ball (x,y), init : placé au milieu de la zone
        self.ballPos = [self.areaRange[0]/2, self.areaRange[1]/2]

        # vector of ball + speed ( [x,y,s])
        self.ballVector = [10, 3, self.defaultSpeed]

        # fonction qui détecte si la balle tocuhe un de la zone

    def isTouched(self, newBallPosition):
        # check si position x de la balle est = a une position d'un bord ( si oui alors ie : elle le touche)

        # Hit top
        if(newBallPosition[0] >= self.topArea[1][0]):
            print("Hit top")
            self.ballVector[0] *= -1
            return True

        # Hit bottom
        elif(newBallPosition[0] <= self.bottomArea[1][0]):
            print("Hit bottom")
            self.ballVector[0] *= -1
            return True

        # Hit left
        elif(newBallPosition[1] <= self.leftArea[0][0]):
            print("Hit left")
            self.ballVector[1] *= -1
            return True

        # Hit right
        elif(newBallPosition[1] >= self.rightArea[0][0]):
            print("Hit right")
            self.ballVector[1] *= -1
            return True

        # No hit
        else:
            return False

        """
                    for i in range(len(self.area)):

            #check x ball hit
            if(self.ballPos[0] in self.area[i][0]):
                self.ballVector[0] *= -1
                return self.ballVector
            
            #check y ball hit
            elif(self.ballPos[1] in self.area[i][1]):
                self.ballVector[0] *= -1
                return self.ballVector
            else:
                return False

        """
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
            print("speed : ", self.ballVector[2], i)
            print("ballposition : ", self.ballPos)
            print("ballVector : ", self.ballVector)
            print("vectorNormalized : ", vectorNormalized)

            tempoBallPosition = [self.ballPos[0] + self.ballVector[0] / vectorNormalized, self.ballPos[1] + self.ballVector[1] / vectorNormalized]

            # isTouched :
            if(self.isTouched(tempoBallPosition) == True):
                print("mur touché !")

            else:
                #la ball ne rentre pas en colision, elle continu son chemin
                self.ballPos = tempoBallPosition
                #return self.ballPos
        return self.ballPos



