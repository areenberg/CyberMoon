# --------------------------------------
#   PREAMPLE
# --------------------------------------

import basicFunctions
from playerEnemyControl import playerEnemyControl
from theMainMenu import theMainMenu
from HighScoreList import HighScoreList
from soundEffects import soundEffects
import sys
import pygame
import pyautogui

# ---------------------------------------
#   METHODS
# ---------------------------------------



# ---------------------------------------
#   INITIAL SETUP
# ---------------------------------------

print(sys.version)

# initialize
pygame.init()
pygame.font.init()

# create surface for the game
monitorWidth, monitorHeight = pyautogui.size()

displayWidth = 1300
displayHeight = 950

if monitorHeight < displayHeight:
    displayHeight = int(monitorHeight * (19.0/20.0))
    displayWidth = int(displayHeight * (4.0/3.0))


gameDisplay = pygame.display.set_mode([displayWidth, displayHeight])

# set the game titles
pygame.display.set_caption('Cyber Moon')
# the game clock
clock = pygame.time.Clock()
# keep the game running
quit = False


# Sound effects and music object
sounds = soundEffects(pygame)

# The Main Menu Object and High Scores
highScoreList = HighScoreList(100)
highScoreList.loadFromFile('cm_hs.json')
mainMenu = theMainMenu(pygame,gameDisplay,highScoreList)

# The Control Object (CO).
# The CO controls all entities and overlay on the current level,
# i.e. what happens to the player, weapons and enemies.
controller = playerEnemyControl(gameDisplay,sounds)


# ---------------------------------------
#   START THE GAME
# ---------------------------------------

while not controller.quitTheGame:

    if mainMenu.menu:
        # jump into the menu
        mainMenu.menuControl(pygame, gameDisplay, controller)
        if mainMenu.startTheGame:
            mainMenu.startTheGame = False
            controller = playerEnemyControl(
                gameDisplay, sounds)  # reset controller

    else:
        # GAME

        # game control
        controller.entityControl(pygame, gameDisplay)
        mainMenu.menu = controller.menuStatus()

    pygame.display.update()
    clock.tick(60)  # DO NOT CHANGE - EVERYTHING IS CALIBRATED TO 60

# quit the game when escaping the while-loop
print("Exiting game")
pygame.quit()
