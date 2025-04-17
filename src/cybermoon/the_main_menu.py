import cybermoon.basic_functions as basic_functions
from cybermoon.menu_shrap import menuShrap
from cybermoon.high_score_list import HighScoreList
import random
import os


class theMainMenu:

    def __init__(self, pygame, gameDisplay, hsList):
        displayDim = gameDisplay.get_size()

        self.startTheGame = False
        self.gameOn = False
        self.menu = True
        self.sub_menu = False
        self.sub_menu_number = 0  # 0: controls, 1: credits, 2: high score
        self.highScoreText = ""
        self.highScoreList = hsList
        self.ButtonFont = pygame.font.SysFont("Helvetica", 34, True, False)
        self.DescriptionFont = pygame.font.SysFont("Helvetica", 28, True, False)
        self.DescriptionSmallFont = pygame.font.SysFont("Helvetica", 14, True, False)
        self.BigHeader = pygame.font.SysFont("Futura Md BT", 72, True, True)
        self.font1 = pygame.font.SysFont("Courier", 72, True, False)
        self.font2 = pygame.font.SysFont("Courier", 30, False, False)

        self.mouseHighlightMode = True
        self.highlightPosition = 0  # which button to highlight in Main Menu
        self.highlightPosition_sub = 0  # Pause Menu
        self.highlightPosition_SubMenu = 0  # Controls and Credits
        self.buttonPositions = [
            int(displayDim[1] * 0.30),
            int(displayDim[1] * 0.42),
            int(displayDim[1] * 0.54),
            int(displayDim[1] * 0.66),
            int(displayDim[1] * 0.78),
        ]  # button positions in main menu

        # main menu big shraps
        self.menuShraps = []

        # pause dynamic color
        self.pcolval = 0
        self.pcolidx = 0
        self.pcoldir = True

    def menuControl(self, pygame, gameDisplay, controller):

        displayDim = gameDisplay.get_size()

        # --------------------------------
        # DRAW AND COLOR
        # -------------------------------
        gameDisplay.fill(basic_functions.defineColors("levelBackground"))

        if not controller.playerAlive:  # DISPLAY GAME OVER IF PLAYER IS DEAD
            self.drawGameOver(pygame, gameDisplay, controller)

        elif not self.gameOn:  # GO TO MAIN MENU IF GAME IS NOT ON

            # draw main menu
            if not self.sub_menu:
                buttontext = self.drawMainMenu(pygame, gameDisplay)
            elif self.sub_menu_number == 0:
                self.drawControls(pygame, gameDisplay)
            elif self.sub_menu_number == 1:
                self.drawCredits(pygame, gameDisplay)
            elif self.sub_menu_number == 2:
                self.drawHighScore(pygame, gameDisplay)

        else:  # DISPLAY PAUSE SCREEN
            cl_sub = [0] * 3
            cl_sub[self.highlightPosition_sub] = 200

            pause_txt = self.BigHeader.render(
                "P   A   U   S   E", False, self.pauseHeaderColor()
            )
            cont_txt = self.ButtonFont.render("Continue", False, (cl_sub[1], 0, 0))
            exit_txt = self.ButtonFont.render("Exit to menu", False, (cl_sub[2], 0, 0))

            gameDisplay.blit(
                pause_txt, (int(displayDim[0] * 0.33), int(displayDim[1] * 0.15))
            )
            gameDisplay.blit(
                cont_txt, (int(displayDim[0] * 0.1), int(displayDim[1] * 0.5))
            )
            gameDisplay.blit(
                exit_txt, (int(displayDim[0] * 0.1), int(displayDim[1] * 0.7))
            )

        # --------------------------------
        # MOUSE ACTIONS
        # --------------------------------
        mspos = pygame.mouse.get_pos()
        if not self.gameOn:
            if not self.sub_menu:
                bhigh = self.pointingToButton(gameDisplay, mspos, buttontext)
                if self.mouseHighlightMode:
                    self.highlightPosition = bhigh
            else:
                bhigh = self.pointingToButton_SubMenus(gameDisplay, mspos)
                if self.mouseHighlightMode:
                    self.highlightPosition_SubMenu = bhigh
        elif self.gameOn and controller.playerAlive:
            bhigh = self.pointingToButton_pauseMenu(gameDisplay, mspos)
            if self.mouseHighlightMode:
                self.highlightPosition_sub = bhigh

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.gameOn:
                    if event.button == 1:
                        if not self.sub_menu:
                            self.mainMenuButtonAction(controller)
                        else:
                            self.subMenuAction(controller)
                elif self.gameOn:
                    if event.button == 1 and controller.playerAlive:
                        self.pauseMenuAction(controller)

            # --------------------------------
            # KEYBOARD ACTIONS
            # --------------------------------

            if event.type == pygame.KEYDOWN:
                if not self.gameOn:
                    if not self.sub_menu:
                        # control for the main menu
                        if event.key == pygame.K_RETURN:  # select highlighted
                            self.mainMenuButtonAction(controller)

                        if (
                            event.key == pygame.K_DOWN
                        ):  # move the highlighted button (using the keyboard)
                            if self.highlightPosition < 4:
                                self.highlightPosition += 1
                                self.mouseHighlightMode = False
                        if event.key == pygame.K_UP:
                            if self.highlightPosition > 1:
                                self.highlightPosition -= 1
                        elif self.highlightPosition == 0:
                            self.highlightPosition = 4
                            self.mouseHighlightMode = False
                    else:
                        # control for sub menus Controls and Credits
                        if event.key == pygame.K_RETURN:
                            self.subMenuAction(controller)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                            self.highlightPosition_SubMenu = 1
                            self.mouseHighlightMode = False
                elif self.gameOn:
                    if event.key == pygame.K_RETURN and controller.playerAlive:
                        self.pauseMenuAction(controller)
                    elif event.key == pygame.K_RETURN and not controller.playerAlive:
                        # print("exit to menu 2")
                        self.addToHighScoreList(controller.score)
                        self.gameOn = False
                        controller.playerAlive = True
                        self.menu = True
                    elif event.key != pygame.K_RETURN and not controller.playerAlive:
                        self.updateHighScoreText(pygame, event)
                    if event.key == pygame.K_DOWN:
                        if self.highlightPosition_sub < 2:
                            self.highlightPosition_sub += 1
                            self.mouseHighlightMode = False
                    if event.key == pygame.K_UP:
                        if self.highlightPosition_sub > 1:
                            self.highlightPosition_sub -= 1
                        if self.highlightPosition_sub == 0:
                            self.highlightPosition_sub = 2
                            self.mouseHighlightMode = False

    def updateHighScoreText(self, pygame, event):
        ls = len(self.highScoreText)
        if ls > 0 and event.key == pygame.K_BACKSPACE:
            self.highScoreText = self.highScoreText[:-1]
        elif (
            ls < 8
            and (pygame.K_a <= event.key <= pygame.K_z)
            or (pygame.K_0 <= event.key <= pygame.K_9)
        ):
            self.highScoreText += event.unicode

    def addToHighScoreList(self, score):
        self.highScoreList.addName(self.highScoreText, score)

    def drawMainMenu(self, pygame, gameDisplay):

        displayDim = gameDisplay.get_size()

        # render the text
        cl = [0] * 6  # number of buttons + 1
        cl[self.highlightPosition] = 200

        header_txt = self.BigHeader.render(
            "C  Y  B  E  R   M  O  O  N", False, (100, 100, 100)
        )
        buttontext = ["Start Game", "High Score", "Controls", "Credits", "Exit Game"]
        playgame_txt = self.ButtonFont.render(buttontext[0], False, (cl[1], 0, 0))
        highscore_txt = self.ButtonFont.render(buttontext[1], False, (cl[2], 0, 0))
        controls_txt = self.ButtonFont.render(buttontext[2], False, (cl[3], 0, 0))
        credits_txt = self.ButtonFont.render(buttontext[3], False, (cl[4], 0, 0))
        exitgame_txt = self.ButtonFont.render(buttontext[4], False, (cl[5], 0, 0))

        # display the text
        gameDisplay.blit(
            header_txt, (int(displayDim[0] * 0.2), int(displayDim[1] * 0.04))
        )
        gameDisplay.blit(
            playgame_txt, (int(displayDim[0] * 0.1), self.buttonPositions[0])
        )
        gameDisplay.blit(
            highscore_txt, (int(displayDim[0] * 0.1), self.buttonPositions[1])
        )
        gameDisplay.blit(
            controls_txt, (int(displayDim[0] * 0.1), self.buttonPositions[2])
        )
        gameDisplay.blit(
            credits_txt, (int(displayDim[0] * 0.1), self.buttonPositions[3])
        )
        gameDisplay.blit(
            exitgame_txt, (int(displayDim[0] * 0.1), self.buttonPositions[4])
        )

        # animate big shraps
        self.animateShraps(pygame, gameDisplay)

        return buttontext

    def drawControls(self, pygame, gameDisplay):

        displayDim = gameDisplay.get_size()

        # render the text
        cl = [0] * 2  # number of buttons + 1
        cl[self.highlightPosition_SubMenu] = 200

        header_txt = self.BigHeader.render("C O N T R O L S", False, (100, 100, 100))
        buttontext = ["Back"]
        backtomenu_txt = self.ButtonFont.render(buttontext[0], False, (cl[1], 0, 0))

        # controls description
        up_txt = self.DescriptionFont.render("W: Move up", False, (200, 200, 200))
        down_txt = self.DescriptionFont.render("S: Move down", False, (200, 200, 200))
        left_txt = self.DescriptionFont.render("A: Move left", False, (200, 200, 200))
        right_txt = self.DescriptionFont.render("D: Move right", False, (200, 200, 200))
        shoot_txt = self.DescriptionFont.render(
            "Left click: Shoot", False, (200, 200, 200)
        )
        pause_txt = self.DescriptionFont.render(
            "Esc: Pause game", False, (200, 200, 200)
        )

        # display the text
        gameDisplay.blit(
            header_txt, (int(displayDim[0] * 0.2), int(displayDim[1] * 0.04))
        )
        gameDisplay.blit(
            backtomenu_txt, (int(displayDim[0] * 0.1), int(displayDim[1] * 0.7))
        )
        gameDisplay.blit(up_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.25)))
        gameDisplay.blit(
            down_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.32))
        )
        gameDisplay.blit(
            left_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.39))
        )
        gameDisplay.blit(
            right_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.46))
        )
        gameDisplay.blit(
            shoot_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.53))
        )
        gameDisplay.blit(
            pause_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.62))
        )

    def drawCredits(self, pygame, gameDisplay):

        displayDim = gameDisplay.get_size()

        # render the text
        cl = [0] * 2  # number of buttons + 1
        cl[self.highlightPosition_SubMenu] = 200

        header_txt = self.BigHeader.render("C R E D I T S", False, (100, 100, 100))
        buttontext = ["Back"]
        backtomenu_txt = self.ButtonFont.render(buttontext[0], False, (cl[1], 0, 0))

        # display the text
        dsc1_txt = self.DescriptionFont.render(
            "Concept design: A. R. Andersen", False, (200, 200, 200)
        )
        dsc2_txt = self.DescriptionFont.render(
            "Programming: A. R. Andersen", False, (200, 200, 200)
        )
        dsc3_txt = self.DescriptionFont.render(
            "Sounds: zapsplat.com", False, (200, 200, 200)
        )
        dsc4_txt = self.DescriptionSmallFont.render(
            "This game is based on the PyGame library (pygame.org).",
            False,
            (200, 200, 200),
        )

        # display the text
        gameDisplay.blit(
            header_txt, (int(displayDim[0] * 0.2), int(displayDim[1] * 0.04))
        )
        gameDisplay.blit(
            backtomenu_txt, (int(displayDim[0] * 0.1), int(displayDim[1] * 0.7))
        )
        gameDisplay.blit(
            dsc1_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.25))
        )
        gameDisplay.blit(
            dsc2_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.32))
        )
        gameDisplay.blit(
            dsc3_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.39))
        )
        gameDisplay.blit(
            dsc4_txt, (int(displayDim[0] * 0.5), int(displayDim[1] * 0.52))
        )

    def drawHighScore(self, pygame, gameDisplay):

        displayDim = gameDisplay.get_size()

        # render the text
        cl = [0] * 2  # number of buttons + 1
        cl[self.highlightPosition_SubMenu] = 200

        header_txt = self.BigHeader.render(
            "H I G H   S C O R E", False, (100, 100, 100)
        )
        buttontext = ["Back"]
        backtomenu_txt = self.ButtonFont.render(buttontext[0], False, (cl[1], 0, 0))

        # display header and button
        gameDisplay.blit(
            header_txt, (int(displayDim[0] * 0.2), int(displayDim[1] * 0.04))
        )
        gameDisplay.blit(
            backtomenu_txt, (int(displayDim[0] * 0.1), int(displayDim[1] * 0.7))
        )

        # calculate positions for high score display
        startY = int(displayDim[1] * 0.25)
        gapY = 50  # gap between each line

        # display each high score
        nameCap = 8  # number of players to display
        for i in range(min(nameCap, len(self.highScoreList.nameList))):
            score_txt = self.DescriptionFont.render(
                f"{i+1}. {self.highScoreList.nameList[i]}: {self.highScoreList.scoreList[i]}",
                False,
                (200, 200, 200),
            )
            gameDisplay.blit(score_txt, (int(displayDim[0] * 0.5), startY + i * gapY))

    def drawGameOver(self, pygame, gameDisplay, controller):

        displayDim = gameDisplay.get_size()

        # all other text
        gameDisplay.fill(basic_functions.defineColors("lightred"))
        txtGameOver = self.font1.render("GAME OVER", False, (0, 0, 0))
        gameDisplay.blit(
            txtGameOver, (int(displayDim[0] * 0.35), int(displayDim[1] * 0.15))
        )
        # txtGameOverSub = self.font2.render('You were killed!', False, (0, 0, 0))

        txtHighScore = self.font2.render(
            "Your name: " + self.highScoreText + "_", False, (0, 0, 0)
        )
        # gameDisplay.blit(txtGameOverSub,(int(displayDim[0]*0.38),int(displayDim[1]*0.50)))
        gameDisplay.blit(
            txtHighScore, (int(displayDim[0] * 0.38), int(displayDim[1] * 0.61))
        )

        # results
        # txtWave = self.font2.render(("You made it to Wave "+str(controller.gameLevel)), False, (0, 0, 0))
        txtScore = self.font2.render(
            ("Score: " + str(controller.score)), False, (0, 0, 0)
        )
        # gameDisplay.blit(txtWave,(int(displayDim[0]*0.35),int(displayDim[1]*0.73)))
        gameDisplay.blit(
            txtScore, (int(displayDim[0] * 0.40), int(displayDim[1] * 0.51))
        )

        numPlace = self.highScoreList.compareToList(controller.score)
        if numPlace == 1:
            numStr = "1st"
        elif numPlace == 2:
            numStr = "2nd"
        elif numPlace == 3:
            numStr = "3rd"
        else:
            numStr = str(numPlace) + "th"
        numStr += " place"
        txtPosition = self.font1.render(numStr, False, (0, 0, 0))
        gameDisplay.blit(
            txtPosition, (int(displayDim[0] * 0.35), int(displayDim[1] * 0.35))
        )

    def startGame(self):

        return self.startTheGame

    def pointingToButton(self, gameDisplay, coord, buttontext):
        displayDim = gameDisplay.get_size()

        button = 0
        for i in range(len(self.buttonPositions)):
            if coord[1] > (self.buttonPositions[i]) and coord[1] < (
                self.buttonPositions[i] + 34
            ):
                if coord[0] > int(displayDim[0] * 0.1) and coord[0] < (
                    int(displayDim[0] * 0.1) + len(buttontext[i]) * 18
                ):
                    button = i + 1
                    self.mouseHighlightMode = True

        return button

    def pointingToButton_pauseMenu(self, gameDisplay, coord):
        displayDim = gameDisplay.get_size()

        b = 0
        if coord[1] > int(displayDim[1] * 0.5) and coord[1] < (
            int(displayDim[1] * 0.5) + 34
        ):
            if coord[0] > int(displayDim[0] * 0.1) and coord[0] < (
                int(displayDim[0] * 0.1) + len("Continue") * 18
            ):
                b = 1
                self.mouseHighlightMode = True
        elif coord[1] > int(displayDim[1] * 0.7) and coord[1] < (
            int(displayDim[1] * 0.7) + 34
        ):
            if coord[0] > int(displayDim[0] * 0.1) and coord[0] < (
                int(displayDim[0] * 0.1) + len("Exit to menu") * 18
            ):
                b = 2
                self.mouseHighlightMode = True

        return b

    def pointingToButton_SubMenus(self, gameDisplay, coord):
        # this method is used for both the Controls and Credits sub menus
        displayDim = gameDisplay.get_size()

        b = 0
        if coord[1] > int(displayDim[1] * 0.7) and coord[1] < (
            int(displayDim[1] * 0.7) + 34
        ):
            if coord[0] > int(displayDim[0] * 0.1) and coord[0] < (
                int(displayDim[0] * 0.1) + len("Back") * 18
            ):
                b = 1
                self.mouseHighlightMode = True

        return b

    def mainMenuButtonAction(self, controller):
        if self.highlightPosition == 1:
            # print("start the game")
            self.startTheGame = True
            self.gameOn = True
            self.menu = False
            self.highlightPosition = 0
            del self.menuShraps[:]
        elif self.highlightPosition == 2:
            # print("open high score")
            self.sub_menu = True
            self.sub_menu_number = 2
        elif self.highlightPosition == 3:
            # print("open controls")
            self.sub_menu = True
            self.sub_menu_number = 0
        elif self.highlightPosition == 4:
            # print("open credits")
            self.sub_menu = True
            self.sub_menu_number = 1
        elif self.highlightPosition == 5:
            # print("quit the game")
            project_root = os.path.dirname(os.path.abspath(__file__))
            self.highScoreList.saveToFile(os.path.join(project_root, "cm_hs.json"))
            controller.quitTheGame = True

    def pauseMenuAction(self, controller):
        if self.highlightPosition_sub == 1:
            # print("continue game")
            self.menu = False
            controller.menu = False
            self.highlightPosition_sub = 0
        elif self.highlightPosition_sub == 2:
            # print("exit to menu 1")
            self.gameOn = False
            controller.playerAlive = True
            self.menu = True
            self.highlightPosition_sub = 0

    def subMenuAction(self, controller):
        if self.highlightPosition_SubMenu == 1:
            # print("exit to menu 1")
            self.menu = True
            self.sub_menu = False
            self.highlightPosition_SubMenu = 0

    def pauseHeaderColor(self):

        speed = 1.5
        if not self.pcoldir and self.pcolval == 0:
            self.pcoldir = True
            if self.pcolidx == 2:
                self.pcolidx = 0
            else:
                self.pcolidx = 2

        if self.pcoldir:
            if (self.pcolval + speed) < 255:
                self.pcolval += speed
            else:
                self.pcolval = 255
                self.pcoldir = False
        elif not self.pcoldir and (self.pcolval - speed) > 0:
            self.pcolval -= speed
        else:
            self.pcolval = 0

        y = [0] * 3
        y[self.pcolidx] = self.pcolval

        return y

    def animateShraps(self, pygame, gameDisplay):
        displayDim = gameDisplay.get_size()

        if not self.menuShraps:
            for i in range(random.randint(1, 10)):
                startPos = [
                    displayDim[0] * random.uniform(0.5, 0.99),
                    displayDim[1] * random.uniform(0.3, 0.99),
                ]
                startDir = random.randint(0, 360)
                self.menuShraps.append(menuShrap(startPos, startDir))
        else:  # animate
            for i in self.menuShraps:
                try:
                    tgt = pygame.mouse.get_pos()
                except:
                    tgt = [displayDim[0] * 0.5, displayDim[1] * 0.5]
                i.drawShrap(pygame, gameDisplay, tgt)
