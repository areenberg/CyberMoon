class soundEffects:

    def __init__(self,pygame):

        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)

        #next level
        self.nextLevel = pygame.mixer.Sound('sounds/nextlevel.wav')

        #obtaining a single shrap
        self.shrapCollected = pygame.mixer.Sound('sounds/obtain1.wav')


    def playShrapCollected(self):
        self.shrapCollected.play()

    def playNextLevel(self):
        self.nextLevel.play()
