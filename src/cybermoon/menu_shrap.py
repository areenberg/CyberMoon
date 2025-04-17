import cybermoon.basic_functions as basic_functions
import math
import random


class menuShrap:
    # NOTE: NOT THE REGULAR SHRAP TYPE. ONLY USED IN MENU.

    def __init__(self, startPos, startDir):
        startDirection = startDir  # start direction in degrees [0,360]
        initRotationSpeed = random.uniform(1, 2)

        self.x = startPos[0]
        self.y = startPos[1]
        self.angle = 0
        self.rotationSpeed = initRotationSpeed
        self.direction = startDirection
        self.initSpeed = 0.5
        self.speed = self.initSpeed
        self.pullSpeed = 0
        self.standardDist = 1

        colors = ["red", "darkGreen", "darkBlue"]
        self.pcolval = basic_functions.defineColors(colors[random.randint(0, 2)])

    def drawShrap(self, pygame, gameDisplay, mousePosition):
        # DRIFT

        # control brake of explosion speed
        pPos = mousePosition
        displayDim = gameDisplay.get_size()

        # driftBrake = 0.0
        # if self.speed>0.1:
        #    self.speed *= 1/(1+driftBrake)
        # else:
        #    self.speed = 0

        deltax = pPos[0] - self.x
        deltay = self.y - pPos[1]
        eucdist = math.sqrt(deltax**2 + deltay**2)
        self.standardDist = eucdist / math.sqrt(displayDim[0] ** 2 + displayDim[1] ** 2)
        pull0 = 0.01
        if self.standardDist > 0.01:
            self.pullSpeed = pull0 / self.standardDist
        else:
            self.pullSpeed = 0

        anglePlayer0 = math.degrees(math.atan(abs(deltay) / abs(deltax)))
        if deltax < 0 and deltay > 0:
            anglePlayer = (180 - anglePlayer0 * 2) + anglePlayer0
            xPull = -self.pullSpeed * math.cos(math.radians(180 - anglePlayer))
            yPull = self.pullSpeed * math.sin(math.radians(180 - anglePlayer))
        elif deltax < 0 and deltay < 0:
            anglePlayer = anglePlayer0 + 180
            xPull = -self.pullSpeed * math.sin(math.radians(270 - anglePlayer))
            yPull = -self.pullSpeed * math.cos(math.radians(270 - anglePlayer))
        elif deltax > 0 and deltay < 0:
            anglePlayer = 360 - anglePlayer0
            xPull = self.pullSpeed * math.cos(math.radians(360 - anglePlayer))
            yPull = -self.pullSpeed * math.sin(math.radians(360 - anglePlayer))
        else:
            anglePlayer = anglePlayer0
            xPull = self.pullSpeed * math.cos(math.radians(anglePlayer))
            yPull = self.pullSpeed * math.sin(math.radians(anglePlayer))

        # control direction
        xCorrection = self.speed * math.cos(math.radians(self.direction)) + xPull
        yCorrection = self.speed * math.sin(math.radians(self.direction)) + yPull

        if (self.x + xCorrection) < displayDim[0] and (self.x + xCorrection) > 0:
            self.x += xCorrection
        elif (self.x + xCorrection) >= displayDim[0]:
            self.direction = 180 - self.direction
        elif (self.x + xCorrection) <= 0:
            self.direction = 180 - self.direction

        if (self.y - yCorrection) > 0 and (self.y - yCorrection) < displayDim[1]:
            self.y -= yCorrection
        elif (self.y - yCorrection) >= displayDim[1]:
            self.direction = 360 - self.direction
        elif (self.y - yCorrection) <= 0:
            self.direction = 360 - self.direction

        # ROTATION
        rotationBrake = 0.0
        if self.rotationSpeed > 0.01:
            # self.rotationSpeed = self.rotationSpeed*(1+rotationBrake)**(-self.nCalled)
            self.rotationSpeed *= 1 / (1 + rotationBrake)
        else:
            self.rotationSpeed = 0

        self.angle += self.rotationSpeed
        sideLength = (1 / 25) * displayDim[0]

        h = (1 / 4) * math.sqrt(3) * sideLength

        A = (
            self.x + math.cos(math.radians(90 - self.angle)) * h,
            self.y - math.sin(math.radians(90 - self.angle)) * h,
        )
        B = (
            self.x + math.cos(math.radians(90 - (self.angle + 120))) * h,
            self.y - math.sin(math.radians(90 - (self.angle + 120))) * h,
        )
        C = (
            self.x + math.cos(math.radians(90 - (self.angle + 240))) * h,
            self.y - math.sin(math.radians(90 - (self.angle + 240))) * h,
        )

        # adjust color
        self.pcolval = list(self.pcolval)
        drc = 1e-6
        self.pcolval[0] -= drc
        self.pcolval[1] -= drc
        self.pcolval[2] -= drc
        self.pcolval[0] = int(self.pcolval[0])
        self.pcolval[1] = int(self.pcolval[1])
        self.pcolval[2] = int(self.pcolval[2])
        self.pcolval = tuple(self.pcolval)

        pygame.draw.polygon(gameDisplay, self.pcolval, (C, B, A), 0)

    def position(self):
        # returns the shrap position

        return [self.x, self.y]
