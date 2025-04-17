import cybermoon.basicFunctions as basicFunctions
import math
import random



class enemy:

    def __init__(self,gameDisplay,startPosition,enemyType,enID):

        #----------------------------
        #movement and animation
        #----------------------------
        displayDim = gameDisplay.get_size()
        self.x = startPosition[0]
        self.y = startPosition[1]

        self.OuterWing = 80 #outer wing dimension

        self.angle_beta = 120 #angle enemy rotated
        self.angle_alpha = 40 #angle wing expansion
        self.expanding = True
        self.speed = 0

        self.alive = True
        self.dead = False
        self.deathInd = -1
        self.dyingCounter = 0
        self.dyingCounterLimit = 330

        #choose enemy color
        self.randomColor()

        #does the entity conduct long turns
        #self.long = False
        #if enemyType==2:
        #    self.long = True

        self.enemyID = enID


    def randomColor(self):
        idx = random.randint(0,3)
        if idx==0:
            self.colout = (0,204,0)
            self.colin = (0,255,0)
        elif idx==1:
            self.colout = (255,0,127)
            self.colin = (153,0,76)
        elif idx==2:
            self.colout = (237,95,242)
            self.colin = (248,58,255)
        elif idx==3:
            self.colout = (252,229,29)
            self.colin = (192,252,29)



    def targeting(self,pygame,gameDisplay,wingAngles,targetPos):

        #---------------------------------------
        #   TARGET
        #---------------------------------------
        displayDim = gameDisplay.get_size()

        targetPosition = targetPos
        minAngle = wingAngles[0]
        maxAngle = wingAngles[1]

        deltax = targetPosition[0]-self.x
        deltay = self.y-targetPosition[1]
        eucdist = math.sqrt(deltax**2 + deltay**2)
        standardDist = eucdist/math.sqrt(displayDim[0]**2+displayDim[1]**2)

        if (deltax==0.0):
            deltax = 1e-6
        angleTarget0 = math.degrees(math.atan(abs(deltay)/abs(deltax)))
        if deltax<0 and deltay>0:
            angleTarget = (180-angleTarget0*2)+angleTarget0

        elif deltax<0 and deltay<0:
            angleTarget = angleTarget0+180

        elif deltax>0 and deltay<0:
            angleTarget = 360-angleTarget0

        else:
            angleTarget = angleTarget0

        #---------------------------------------
        #   MOVEMENT
        #---------------------------------------

        startSpeed = 8
        rotationSpeed = 0.9

        if (self.angle_beta+180)<=360:
            angBeta = self.angle_beta+180
        else:
            angBeta = self.angle_beta+180-360

        if min(abs(angleTarget-angBeta),(360-abs(angleTarget-angBeta)))>45:

            #adjust parameters if target within turn radius
            turnRad = startSpeed/math.radians(rotationSpeed)
            if eucdist<turnRad:
                startSpeed = 7
                rotationSpeed = math.degrees(startSpeed/eucdist)


            #find the shortest turn
            positiveTurn = False
            if (angBeta>180 and ((angleTarget>angBeta and
             angleTarget>self.angle_beta) or (angleTarget<angBeta and
              angleTarget<self.angle_beta))) or (angBeta<180 and
               (angleTarget>angBeta and angleTarget<self.angle_beta)):
                positiveTurn = True

            #invert direction if long turns and enemy is close
            #if self.long and standardDist<0.30 and standardDist>0.15:
            #    if positiveTurn:
            #        positiveTurn = False
            #    else:
            #        positiveTurn = True

            #make the turn
            if positiveTurn:
                self.angle_beta += rotationSpeed
                if self.angle_beta>360:
                    self.angle_beta -= 360
            else:
                self.angle_beta -= rotationSpeed
                if self.angle_beta<0:
                    self.angle_beta += 360

        if self.angle_alpha<maxAngle and self.expanding: #charge
            self.angle_alpha += 0.45
        elif self.angle_alpha>minAngle and self.expanding==False: #move forward
            self.angle_alpha -= 0.04*self.angle_alpha
            self.speed = startSpeed
        elif self.angle_alpha>=maxAngle and self.expanding:
            self.expanding = False
        elif self.angle_alpha<=minAngle and self.expanding==False:
            self.expanding = True

        #movement
        self.x -= math.cos(math.radians(self.angle_beta))*self.speed
        self.y += math.sin(math.radians(self.angle_beta))*self.speed
        driftBrake = 0.05
        if self.speed<1e-3:
            self.speed = 0
        else:
            self.speed *= 1/(1+driftBrake)



    def animateMovement(self,pygame,gameDisplay,wingAngles):

        #---------------------------------------
        #   ANIMATION
        #---------------------------------------

        minAngle = wingAngles[0]
        maxAngle = wingAngles[1]

        #wing left
        x0 = self.x
        y0 = self.y
        beta = self.angle_beta
        alpha = self.angle_alpha
        gamma = 180-(alpha+beta)

        wingAngleFraction = (alpha - minAngle)/(maxAngle - minAngle)

        a = self.OuterWing #outer wing dimension
        b = 40 #wing dimension towards body
        c1 = b*1.50 #tail tip
        c2 = b*0.80 #tail beginning
        c3 = b*0.50 #tail width


        A = (x0,y0)
        B = (x0+math.cos(math.radians(beta))*b,y0-math.sin(math.radians(beta))*b)
        C = (x0 - math.cos(math.radians(gamma))*a,y0 - math.sin(math.radians(gamma))*a)

        pygame.draw.polygon(gameDisplay, basicFunctions.enemyColor(wingAngleFraction,self.colout,self.colin),
        (C,B,A),0)

        #wing right
        alpha = -self.angle_alpha
        gamma = 180-(alpha+beta)

        B = (x0+math.cos(math.radians(beta))*b,y0-math.sin(math.radians(beta))*b)
        C = (x0 - math.cos(math.radians(gamma))*a,y0 - math.sin(math.radians(gamma))*a)

        pygame.draw.polygon(gameDisplay, basicFunctions.enemyColor(wingAngleFraction,self.colout,self.colin),
        (C,B,A),0)

        #tail
        A = (x0+math.cos(math.radians(beta))*c1,y0-math.sin(math.radians(beta))*c1)
        B = (x0+math.cos(math.radians(beta-math.degrees(math.atan(0.5*c3/c2))))*math.sqrt(c2**2+(0.5*c3)**2),
        y0-math.sin(math.radians(beta-math.degrees(math.atan(0.5*c3/c2))))*math.sqrt(c2**2+(0.5*c3)**2))
        C = (B[0]-math.cos(math.radians(90-beta))*c3,B[1]-math.sin(math.radians(90-beta))*c3)

        pygame.draw.polygon(gameDisplay, basicFunctions.enemyColor(wingAngleFraction,self.colout,self.colin),
        (C,B,A),0)


    def drawEnemy(self,pygame,gameDisplay,targetPosition):

        displayDim = gameDisplay.get_size()

        #wing movement
        maxAngle = 50
        minAngle = 25

        if self.alive: #if the enemy is alive

            #target player (orientation and adaptation relative to player position)
            self.targeting(pygame,gameDisplay,[minAngle,maxAngle],targetPosition)

            #animate the enemy
            self.animateMovement(pygame,gameDisplay,[minAngle,maxAngle])

        elif self.dyingCounter<self.dyingCounterLimit:
            #the enemy is dying
            #print("ENEMY DYING")
            self.dyingCounter += 1

            self.updateExplosion(pygame,gameDisplay)

        else:
            #print("ENEMY DEAD")
            self.dead = True


    def evaluateDeath(self,grenadeObjects,shotInd):
        #evaluate distance and mortality of all shraps

        #----FOR TESTING----
        #self.initializeExplosion()
        #self.alive = False
        #-------------------
        for g in grenadeObjects:
            shrapPos = g.shrapPositions()
            deadly = g.shrapDeadly()

            for i in range(len(shrapPos)):
                deltax = shrapPos[i][0]-self.x
                deltay = shrapPos[i][1]-self.y
                eucdist = math.sqrt(deltax**2 + deltay**2)
                if eucdist<(self.OuterWing*0.9) and deadly[i] and self.alive:
                    #initial parameters for "death explosion"
                    self.initializeExplosion()
                    self.alive = False
                    self.deathInd=shotInd
                    

    def isDead(self):
    #returns True if the enemy is dead; otherwise False

        return self.dead

    def isAlive(self):
    #returns True if the enemy is alive; otherwise False

        return self.alive



    def initializeExplosion(self):
        self.deathOrigin = [self.x,self.y]
        n_particles = 100
        colors = ["black","pink","green","blue"]

        self.part_pos = [] #current coordinates of particles
        self.part_dir = [] #direction of particle in degrees
        self.part_col = [] #particle color
        self.particleSpeed = [] #particles initial speed
        for i in range(n_particles):
            rngl = random.randrange(0,36000000000)
            randAngle = rngl/100000000
            rndSpd = random.randrange(11000,14000)
            randSpeed = rndSpd/1000
            rColIdx = random.randrange(0,4)
            randColor = colors[rColIdx]
            self.particleSpeed.append(randSpeed)
            self.part_dir.append(randAngle)
            self.part_pos.append([self.x,self.y])
            self.part_col.append(randColor)

    def updateExplosion(self,pygame,gameDisplay):

        displayDim = gameDisplay.get_size()
        dspl_hypo = math.sqrt(displayDim[0]**2+displayDim[1]**2)
        n_particles = len(self.part_dir)#print(self.particleSpeed,xx,yy)

        driftBrake = 0.05
        pull = 0.07


        #update position
        for p in range(n_particles):

            #replacement from explosion
            if self.particleSpeed[p]>0.01:
                self.part_pos[p][0] += self.particleSpeed[p]*math.cos(math.radians(self.part_dir[p]))
                self.part_pos[p][1] -= self.particleSpeed[p]*math.sin(math.radians(self.part_dir[p]))
                self.particleSpeed[p] *= 1/(1+driftBrake) #update speed
            else:
                self.particleSpeed[p] = 0

            #replacement from pull
            deltaxx = self.part_pos[p][0]-self.deathOrigin[0]
            deltayy = self.part_pos[p][1]-self.deathOrigin[1]
            euc_dist = math.sqrt(deltaxx**2 + deltayy**2)
            euc_standardDist = euc_dist/dspl_hypo

            if euc_standardDist>0.005:
                pullSpeed = pull/euc_standardDist
            else:
                pullSpeed = 0
            pullDir = self.part_dir[p]+180
            if pullDir>360:
                pullDir -= 360
            self.part_pos[p][0] += pullSpeed*math.cos(math.radians(pullDir))
            self.part_pos[p][1] -= pullSpeed*math.sin(math.radians(pullDir))


        #draw particles
        for p in range(n_particles):
            pygame.draw.circle(gameDisplay, basicFunctions.defineColors("darkGreen"),
            [math.floor(self.deathOrigin[0]),math.floor(self.deathOrigin[1])], 3)

            pygame.draw.circle(gameDisplay, basicFunctions.defineColors(self.part_col[p]),
            [math.floor(self.part_pos[p][0]),math.floor(self.part_pos[p][1])], 2)


    def position(self):
        #returns the position

        return [self.x,self.y]
