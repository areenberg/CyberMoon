import cybermoon.basicFunctions as basicFunctions
from cybermoon.grenade import grenade
import math


class Player:

    def __init__(self,gameDisplay,soundObject):

        #----------------------------
        #movement and animation
        #----------------------------
        displayDim = gameDisplay.get_size()
        self.x = math.ceil(displayDim[0]*0.5)
        self.y = math.ceil(displayDim[1]*0.5)
        self.height = math.ceil(displayDim[0]*(1.0/40.0))
        self.width = self.height
        #player tilt
        self.tilt = 0
        self.tiltMax = 30
        self.tiltChange = 0.5
        self.tiltBrake = self.tiltChange*0.8
        self.moveTimer = 0
        #mouse position
        self.mousex = 0
        self.mousey = 0
        #player color
        self.pcolval = basicFunctions.defineColors("playerColor")
        self.pcolvaldir = 1
        #sounds
        self.sounds = soundObject

        #----------------------------
        #ammo and health
        #----------------------------

        self.grenades = []
        self.maxAmmo = 1
        self.availableGrenades = self.maxAmmo
        self.shrapCollected = 0
        self.numberofShraps = 5 #number of shraps per grenade
        self.currentInd = 0 #multikill tracking (counts the number of shots)

    def updateMovement(self,keys,pygame,gameDisplay):
        #updates player actions (e.g. the position)
        displayDim = gameDisplay.get_size()


        if keys[pygame.K_w]:
            if (self.y-5)>0:
                self.y -= 5
        if keys[pygame.K_s]:
            if (self.y+5)<displayDim[1]:
                self.y += 5
        if keys[pygame.K_a]:
            if (self.x-5)>0:
                self.x -= 5

                if (self.tilt-self.tiltChange)>-self.tiltMax:
                    self.tilt -= self.tiltChange
                    #updated whenever the player has moved
                    self.moveTimer = 2

        if keys[pygame.K_d]:
            if (self.x+5)<displayDim[0]:
                self.x += 5

            if (self.tilt+self.tiltChange)<self.tiltMax:
                self.tilt += self.tiltChange
                #updated whenever the player has moved
                self.moveTimer = 2


    def actions(self,pygame,event,gameDisplay):

        #if event.type == pygame.MOUSEMOTION:
        #    self.mousex, self.mousey = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            self.availableGrenades += math.floor(self.shrapCollected/self.numberofShraps)
            self.shrapCollected -= math.floor(self.shrapCollected/self.numberofShraps)*self.numberofShraps

            if self.availableGrenades>0:
                self.grenades.append(grenade(gameDisplay,[self.x,self.y],event.pos,self.numberofShraps,self.sounds))
                self.availableGrenades -= 1
                self.currentInd += 1 

    def adjustPlayerColor(self):

        self.pcolval = list(self.pcolval)

        if (self.pcolval[0]+self.pcolvaldir)<160 or (self.pcolval[0]+self.pcolvaldir)>=255:
            self.pcolvaldir *= -1

        if (self.pcolval[1]+self.pcolvaldir)<160 or (self.pcolval[1]+self.pcolvaldir)>=255:
            self.pcolvaldir *= -1

        self.pcolval[0] += self.pcolvaldir
        self.pcolval[1] += self.pcolvaldir

        self.pcolval = tuple(self.pcolval)

    def drawPlayer(self,pygame,gameDisplay):

        #updates the player in the game
        alpha = math.radians(45-self.tilt)
        hypon = self.height/math.sqrt(2)
        cos1 = math.cos(alpha)*hypon
        sin1 = math.sin(alpha)*hypon
        A = (self.x+cos1,self.y+sin1)
        B = (self.x+sin1,self.y-cos1)
        C = (self.x-cos1,self.y-sin1)
        D = (self.x-sin1,self.y+cos1)

        self.adjustPlayerColor()
        pygame.draw.polygon(gameDisplay, self.pcolval,
        (D,C,B,A),0)

        #reverse tilt
        if self.moveTimer==0:
            if self.tilt>0:
                self.tilt -= self.tiltBrake
            if self.tilt<0:
                self.tilt += self.tiltBrake
            if abs(self.tilt)<0.5:
                self.tilt *= 0.1
        elif self.moveTimer>0:
                self.moveTimer -= 1


    def drawWeapons(self,pygame,gameDisplay):

        playerPosition = [self.x,self.y]
        rmv = []

        if self.grenades:
            kk = 0

            for g in self.grenades:
                g.drawGrenade(pygame,gameDisplay,playerPosition)
                self.shrapCollected += g.shrapCollection() #move shraps from grenade to player
                g.shrapRemoval(g.shrapCollection())
                if g.activeShraps() == 0:
                    rmv.append(kk)
                kk += 1

        if rmv:
            for i in range(len(rmv)):
                del self.grenades[rmv[i]] #delete grenade object
                if i < (len(rmv)-1):
                    for j in range((i+1),len(rmv)):
                        rmv[j] -= 1


    def position(self):
        #returns the player position

        return [self.x,self.y]

    def getGrenades(self):
        #returns all (active) grenade objects

        return self.grenades
