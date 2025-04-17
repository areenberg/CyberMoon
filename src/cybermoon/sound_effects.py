import os


class soundEffects:

    def __init__(self, pygame):

        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)
        project_root = os.path.dirname(os.path.abspath(__file__))

        # next level
        self.nextLevel = pygame.mixer.Sound(
            os.path.join(project_root, "sounds/nextlevel.wav")
        )

        # obtaining a single shrap
        self.shrapCollected = pygame.mixer.Sound(
            os.path.join(project_root, "sounds/obtain1.wav")
        )

    def playShrapCollected(self):
        self.shrapCollected.play()

    def playNextLevel(self):
        self.nextLevel.play()
