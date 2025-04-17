import cybermoon.basicFunctions as basicFunctions
import math
import random

class shrap:


    def __init__(self,startPos,startDirection,initRotationSpeed):
        #startDirection = random.uniform(0,360)
        #initRotationSpeed = random.uniform(50,65)

        self.x = startPos[0]
        self.y = startPos[1]
        self.angle = 0
        self.rotationSpeed = initRotationSpeed
        self.direction = startDirection
        self.initSpeed = 10
        self.speed = self.initSpeed
        self.playerPullSpeed = 0
        self.standardDist = 1

    def drawShrap(self,pygame,gameDisplay,playerPosition):
        #DRIFT

        #control brake of explosion speed
        displayDim = gameDisplay.get_size()

        driftBrake = 0.01
        #self.nCalled += 1
        if self.speed>0.1:
            #self.speed = self.initSpeed*(1+driftBrake)**(-self.nCalled)
            self.speed *= 1/(1+driftBrake)
        else:
            self.speed = 0

        deltax = playerPosition[0]-self.x
        deltay = self.y-playerPosition[1]
        eucdist = math.sqrt(deltax**2 + deltay**2)
        self.standardDist = eucdist/math.sqrt(displayDim[0]**2+displayDim[1]**2)
        pull0 = 0.08
        if self.standardDist>0.01:
            self.playerPullSpeed = pull0/self.standardDist
        else:
            self.playerPullSpeed = 0

        anglePlayer0 = math.degrees(math.atan(abs(deltay)/abs(deltax)))
        if deltax<0 and deltay>0:
            anglePlayer = (180-anglePlayer0*2)+anglePlayer0
            xPull = -self.playerPullSpeed*math.cos(math.radians(180-anglePlayer))
            yPull = self.playerPullSpeed*math.sin(math.radians(180-anglePlayer))
        elif deltax<0 and deltay<0:
            anglePlayer = anglePlayer0+180
            xPull = -self.playerPullSpeed*math.sin(math.radians(270-anglePlayer))
            yPull = -self.playerPullSpeed*math.cos(math.radians(270-anglePlayer))
        elif deltax>0 and deltay<0:
            anglePlayer = 360-anglePlayer0
            xPull = self.playerPullSpeed*math.cos(math.radians(360-anglePlayer))
            yPull = -self.playerPullSpeed*math.sin(math.radians(360-anglePlayer))
        else:
            anglePlayer = anglePlayer0
            xPull = self.playerPullSpeed*math.cos(math.radians(anglePlayer))
            yPull = self.playerPullSpeed*math.sin(math.radians(anglePlayer))


        #control direction
        xCorrection = self.speed*math.cos(math.radians(self.direction))+xPull
        yCorrection = self.speed*math.sin(math.radians(self.direction))+yPull

        if ((self.x+xCorrection)<displayDim[0] and (self.x+xCorrection)>0):
            self.x += xCorrection
        elif (self.x+xCorrection)>=displayDim[0]:
            self.direction = 180-self.direction
        elif (self.x+xCorrection)<=0:
            self.direction = 180-self.direction

        if ((self.y-yCorrection)>0 and (self.y-yCorrection)<displayDim[1]):
            self.y -= yCorrection
        elif (self.y-yCorrection)>=displayDim[1]:
            self.direction = 360-self.direction
        elif (self.y-yCorrection)<=0:
            self.direction = 360-self.direction

        #ROTATION
        rotationBrake = 0.01
        if self.rotationSpeed>0.01:
            #self.rotationSpeed = self.rotationSpeed*(1+rotationBrake)**(-self.nCalled)
            self.rotationSpeed *= 1/(1+rotationBrake)
        else:
            self.rotationSpeed = 0


        self.angle += self.rotationSpeed
        sideLength = (1/100)*displayDim[0]

        h = (1/4)*math.sqrt(3)*sideLength

        A = (self.x+math.cos(math.radians(90-self.angle))*h,self.y-math.sin(math.radians(90-self.angle))*h)
        B = (self.x+math.cos(math.radians(90-(self.angle+120)))*h,self.y-math.sin(math.radians(90-(self.angle+120)))*h)
        C = (self.x+math.cos(math.radians(90-(self.angle+240)))*h,self.y-math.sin(math.radians(90-(self.angle+240)))*h)

        pygame.draw.polygon(gameDisplay, basicFunctions.cool(self.rotationSpeed),
        (C,B,A),0)

    def position(self):
        #returns the shrap position

        return [self.x,self.y]

    def distToPlayer(self):
        #returns the standardized distance to the player

        return self.standardDist

    def isDeadly(self):
        #returns if the shrap will be deadly if touched by the enemy

        deadly = False
        if self.speed > (self.initSpeed*0.60):
            deadly = True

        return deadly
