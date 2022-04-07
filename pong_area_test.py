#fichier de test

#actu : test les colisions


from fps_limiter import LimitFPS, FPSCounter

fps_limiter = LimitFPS(fps=5)
fps_counter = FPSCounter()


class gameInit:
    def __init__(self,areaRange):
        self.areaRange = areaRange

        """
        représentation des coordonnées des segments:

        ((x.left,x.right), (y.left,y.right))
        """

        self.topArea = ( (0,self.areaRange[0]) , (self.areaRange[1],self.areaRange[1]) )
        self.bottomArea = ( (0,self.areaRange[0]) , (0,0) )
        self.leftArea = ( (0,0) , (0,self.areaRange[1]) )
        self.rightArea = ( (self.areaRange[0],self.areaRange[0]) , (self.areaRange[1],self.areaRange[1]) ) 

        self.area = [self.topArea, self.bottomArea, self.leftArea, self.rightArea]

        #initialisation de la ball

        #position ball (x,y), init : placé au milieu de la zone
        self.ballPos = [self.areaRange[0]/2, self.areaRange[1]/2]

        #vector of ball + speed ( [x,y,s])
        self.ballVector = [10,0,1]


        #fonction qui détecte si la balle tocuhe un de la zone
        def isTouched(ball_pos):

            #check si position x de la balle est = a une position d'un bord ( si oui alors ie : elle le touche)
            for i in range(len(self.area)):

                #check x ball hit
                if(ball_pos[0] in self.area[i][0]):
                    return newBallVector(i)
                
                #check y ball hit
                elif(ball_pos[1] in self.area[i][1]):
                    return newBallVector(i)
                else:
                    return False

        #calcule the new vector ball after isTouched

        def newBallVector(index):
            """
            on calule dans un premier temps l'angle auquel la balle touche le mur

                -savoir si le mur est horizontale ou verticale
                -on prend un vecteur perpendiculaire au mur
                -on calcule le nouveaux vecteur avec ca ^^
            
            """

            #
            
            wallHitLine = ( self.area[index][0][1] - self.area[index][0][0], self.area[index][1][1] - self.area[index][1][0] )
            wallHitVectorPerpendicualarLine = 0





while True:
    if fps_limiter():
        
        
        print("current fps: %s" % fps_counter())