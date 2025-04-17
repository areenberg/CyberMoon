from cybermoon.player import Player
from cybermoon.enemy import enemy
import cybermoon.basic_functions as basic_functions
import math
import random


class playerEnemyControl:
    # the player and enemy control object

    def __init__(self, gameDisplay, soundObject):
        # INITIAL GAME CONDITIONS

        # level
        self.gameLevel = 0  # will increase to 1 immediately after start
        self.newLevel = True

        # player
        self.player = Player(gameDisplay, soundObject)
        self.playerAlive = True

        # go to game instead of menu
        self.menu = False
        self.quitTheGame = False

        # performance metrics
        self.enemiesTotalKill = 0
        self.score = 0
        self.multiKill = 1  # starts at 1
        self.lastInd = -1  # multikill tracking

        # sounds
        self.sounds = soundObject

        # point system
        self.baseKillPoints = 50

    def entityControl(self, pygame, gameDisplay):

        # reset screen
        if self.playerAlive:
            gameDisplay.fill(basic_functions.defineColors("levelBackground"))
        else:
            self.menu = True

        # keys pressed
        keys = pygame.key.get_pressed()

        # -----------------------------------------
        #               LEVEL
        # -----------------------------------------

        self.levelCreater(gameDisplay)

        # -----------------------------------------
        #               PLAYER
        # -----------------------------------------
        self.player.updateMovement(keys, pygame, gameDisplay)
        self.player.drawPlayer(pygame, gameDisplay)  # update player position
        self.player.drawWeapons(pygame, gameDisplay)  # update weapon dynamics

        self.evaluatePlayerDeath(gameDisplay)

        self.playerActions(pygame, gameDisplay)

        # ----------------------------------------
        #               ENEMIES
        # ----------------------------------------

        if self.enemyList:
            delIdx = []
            self.getEnemyBehavior(pygame, gameDisplay)
            for enIdx in range(len(self.enemyList)):
                en = self.enemyList[enIdx]

                en.drawEnemy(
                    pygame,
                    gameDisplay,
                    self.getEnemyTarget(
                        pygame,
                        gameDisplay,
                        len(self.enemyList),
                        self.player.position(),
                        en,
                    ),
                )

                en.evaluateDeath(self.player.getGrenades(), self.player.currentInd)
                if en.isDead():
                    delIdx.append(enIdx)
            # delete deaths
            if delIdx:
                for i in range(len(delIdx)):

                    self.enKilled += 1
                    self.enemiesTotalKill += 1
                    self.score += self.baseKillPoints
                    if self.lastInd == self.enemyList[delIdx[i]].deathInd:
                        self.multiKill += 1
                    else:
                        self.lastInd = self.enemyList[delIdx[i]].deathInd

                    del self.enemyList[delIdx[i]]

                    # print("Enemy killed. Level enemies left:",self.enemyNumber-self.enKilled)

                    if self.enKilled == self.enemyNumber:
                        # print("LEVEL",self.gameLevel,"COMPLETED")
                        self.newLevel = True
                    if i < (len(delIdx) - 1):
                        for j in range((i + 1), len(delIdx)):
                            delIdx[j] -= 1

            if self.multiKill > 1 and self.allEnemiesAlive():
                multPoints = (
                    self.baseKillPoints * self.multiKill**2
                    - self.baseKillPoints * self.multiKill
                )
                # print("Multikills:",self.multiKill)
                self.score += multPoints
                self.multiKill = 1

        # -----------------------------------------
        #               OVERLAY
        # -----------------------------------------

        self.gameOverlay(pygame, gameDisplay)

    def playerActions(self, pygame, gameDisplay):

        # shooting and quiting
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.actions(pygame, event, gameDisplay)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # print("Go to menu")
                    # self.quitTheGame = True
                    self.menu = True

    def evaluatePlayerDeath(self, gameDisplay):
        if self.enemyList:
            pos_pl = self.player.position()
            for enIdx in range(len(self.enemyList)):
                en = self.enemyList[enIdx]
                pos_e = en.position()

                # calculate the standardized distance
                dist = self.stdDistance(pos_pl, pos_e, gameDisplay)

                # distance threshold
                threshold = 0.01
                if dist < threshold:
                    self.playerAlive = False
                    # print("PLAYER DEAD")

    def stdDistance(self, pos1, pos2, gameDisplay):
        # returns the standardized distance between
        # two objects

        displayDim = gameDisplay.get_size()

        deltaxx = pos1[0] - pos2[0]
        deltayy = pos1[1] - pos2[1]

        euc_dist = math.sqrt(deltaxx**2 + deltayy**2)
        dspl_hypo = math.sqrt(displayDim[0] ** 2 + displayDim[1] ** 2)
        euc_standardDist = euc_dist / dspl_hypo

        return euc_standardDist

    def levelCreater(self, gameDisplay):

        if self.newLevel:
            self.gameLevel += 1
            # print("BEGIN LEVEL",self.gameLevel)
            if self.gameLevel > 1:
                self.sounds.playNextLevel()
            # number of enemies that needs to be
            # killed at the current level
            self.enemyNumber = math.ceil(self.gameLevel**1.5)
            self.enAppTime = [0] * int(self.enemyNumber)

            if self.enemyNumber > 1:
                # time between enemies
                rate = 0.016 - 0.016 * 0.9 * (1 / self.gameLevel)
                for i in range(1, len(self.enAppTime)):
                    r = random.uniform(0, 1)
                    self.enAppTime[i] = math.ceil(-(math.log(1 - r) / rate))

            self.enIdx = 0
            self.enTime = self.enAppTime[self.enIdx]
            self.enemyList = []
            self.newLevel = False
            self.enKilled = 0

        # create new enemies
        if self.enTime == 0 and self.enIdx < self.enemyNumber:
            # create the enemy
            rdir = random.randrange(0, 365)
            hsh = math.sqrt(
                (gameDisplay.get_size()[0] * 0.5) ** 2
                + (gameDisplay.get_size()[1] * 0.5) ** 2
            )
            x = hsh * math.cos(math.radians(rdir)) + gameDisplay.get_size()[0] * 0.5
            y = hsh * math.sin(math.radians(rdir)) + gameDisplay.get_size()[1] * 0.5
            entype = self.getEnemyType()
            self.enemyList.append(
                enemy(gameDisplay, [x, y], entype, random.randint(10000, 99999))
            )
            self.enIdx += 1
            # get time for next enemy
            if self.enIdx < self.enemyNumber:
                self.enTime = self.enAppTime[self.enIdx]
        if self.enTime > 0:
            self.enTime -= 1

    def menuStatus(self):

        return self.menu

    def playerStatus(self):

        return self.playerAlive

    def statusQuit(self):

        return self.quitTheGame

    def gameOverlay(self, pygame, gameDisplay):
        displayDim = gameDisplay.get_size()

        # overlay font
        ft = pygame.font.SysFont("liberationmono", 34, True, False)
        ft2 = pygame.font.SysFont("liberationmono", 28, True, False)

        # wave number
        wavetxt = ft.render(("Wave " + str(self.gameLevel)), False, (192, 192, 192))
        gameDisplay.blit(
            wavetxt, (int(displayDim[0] * 0.05), int(displayDim[1] * 0.04))
        )

        # enemy count
        enemtxt = ft2.render(("Score " + str(self.score)), False, (192, 192, 192))
        gameDisplay.blit(
            enemtxt, (int(displayDim[0] * 0.80), int(displayDim[1] * 0.05))
        )

        return 0

    def getEnemyType(self):
        type = 1
        # if self.gameLevel>2:
        #    r = random.uniform(0,1)
        #    if r<0.20:
        #        type = 2

        return type

    def getEnemyBehavior(self, pygame, gameDisplay):

        all_pos = []
        pos_x = 0
        pos_y = 0
        for enIdx in range(len(self.enemyList)):
            en = self.enemyList[enIdx]
            all_pos.append(en.position())
            pos_x += en.position()[0]
            pos_y += en.position()[1]
        pos_x /= len(self.enemyList)
        pos_y /= len(self.enemyList)
        self.avgEnPos = [int(pos_x), int(pos_y)]

        # uncomment to show average enemy position on screen
        # pygame.draw.circle(gameDisplay, basicFunctions.defineColors("blue"),
        # self.avgEnPos, 3)

    def getEnemyTarget(self, pygame, gameDisplay, nEnemies, playerPos, enemy):

        newTarget = playerPos
        eucd = math.sqrt(
            (enemy.position()[0] - self.avgEnPos[0]) ** 2
            + (enemy.position()[1] - self.avgEnPos[1]) ** 2
        )
        if eucd < 200:
            random.seed(enemy.enemyID)
            if nEnemies > 3 and nEnemies < 8:
                newTarget[0] += random.randint(-500, 500)
                newTarget[1] += random.randint(-500, 500)
            elif nEnemies > 8:
                newTarget[0] += random.randint(-1000, 1000)
                newTarget[1] += random.randint(-1000, 1000)

        # uncomment to show enemy target on screen
        # pygame.draw.circle(gameDisplay, basicFunctions.defineColors("red"),
        # newTarget, 3)

        return newTarget

    def allEnemiesAlive(self):
        k = 0
        for en in self.enemyList:
            if en.isAlive():
                k += 1
        if k == len(self.enemyList):
            return True
        else:
            return False


#    def shrapsCooled(self,grenadeObjects):
#        #returns true if none of the current shraps
#        #are lethal
#
#        d=0
#        k=0
#        for g in grenadeObjects:
#            shrapPos = g.shrapPositions()
#            deadly = g.shrapDeadly()
#            for i in range(len(shrapPos)):
#                k+=1
#                if not deadly[i]:
#                    d+=1
#        if k==d:
#            return(True)
#        else:
#            return(False)
