import cybermoon.basic_functions as basic_functions
import math
import random
import os
from cybermoon.shrap import shrap


class grenade:

    def __init__(self, gameDisplay, startPos, targetPos, genShraps, soundObject):

        self.x = startPos[0]
        self.y = startPos[1]
        self.x1 = targetPos[0]
        self.y1 = targetPos[1]

        self.lifeTime = 100
        self.timer = self.lifeTime
        self.temp = 0
        self.sh = []

        displayDim = gameDisplay.get_size()
        self.grenadeSize = math.ceil(displayDim[0] * (1.0 / 200.0))

        self.numberofShraps = genShraps
        random.seed(os.urandom(16))
        self.startDirection = [
            random.uniform(0, 360) for _ in range(self.numberofShraps)
        ]
        self.initRotationSpeed = [
            random.uniform(50, 65) for _ in range(self.numberofShraps)
        ]

        # shrap collection
        self.collected = 0
        self.activeSh = self.numberofShraps

        # sounds
        self.sounds = soundObject

    def drawGrenade(self, pygame, gameDisplay, playerPosition):
        if self.timer > -1:  # count down
            self.timer -= 1
            self.temp += 1
            # print(self.timer)

            # update grenade position
            displayDim = gameDisplay.get_size()
            maxSpeed = 100
            a = 1.1
            self.x = self.x + (maxSpeed * (self.x1 - self.x) / displayDim[0]) * a ** (
                -self.temp
            )
            self.y = self.y + (maxSpeed * (self.y1 - self.y) / displayDim[0]) * a ** (
                -self.temp
            )
            pygame.draw.circle(
                gameDisplay,
                basic_functions.glow(self.temp, self.lifeTime),
                [math.floor(self.x), math.floor(self.y)],
                self.grenadeSize,
            )

        if self.timer == 0:  # explosion
            # generate a bunch of shraps
            for s in range(self.numberofShraps):
                self.sh.append(
                    shrap(
                        [self.x, self.y],
                        self.startDirection[s],
                        self.initRotationSpeed[s],
                    )
                )

        if self.timer < 0:

            # control of shraps after the explosion
            rmv = []
            kk = 0
            for s in self.sh:  # animate shrap metal
                s.drawShrap(pygame, gameDisplay, playerPosition)
                # check distance
                dist = s.distToPlayer()
                if dist <= 0.01:
                    self.sounds.playShrapCollected()
                    rmv.append(kk)

                kk += 1
            if rmv:
                for i in range(len(rmv)):
                    del self.sh[rmv[i]]  # delete shrap objects from grenade
                    if i < (len(rmv) - 1):
                        for j in range((i + 1), len(rmv)):
                            rmv[j] -= 1
                    self.collected += 1
                    self.activeSh -= 1

    def shrapCollection(self):
        # number of shraps collected for this specific grenade

        return self.collected

    def shrapRemoval(self, numberRemove):
        # remove collected shraps for the grenade
        self.collected -= numberRemove

    def activeShraps(self):
        # number of shraps generated on explosions

        return self.activeSh

    def shrapPositions(self):
        # position of all shraps controlled by the grenade

        positions = []
        for s in self.sh:
            positions.append(s.position())

        return positions

    def shrapDeadly(self):
        # boolean list showing if a particular shrap is deadly
        # (true if yes)

        deadly = []
        for s in self.sh:
            deadly.append(s.isDeadly())

        return deadly
