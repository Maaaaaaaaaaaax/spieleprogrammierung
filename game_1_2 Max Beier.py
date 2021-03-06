import pygame
import os
import random

class Settings(object):
    width = 700
    height = 400
    fps = 60
    title = "Game_1_2"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

class Racer(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "racer01.png")).convert_alpha() # Bild wird mit Alphakanal geladen
        self.image = pygame.transform.scale(self.image, (45, 42))
        self.rect = self.image.get_rect()                           # Setzt ein Rechteck um das Auto, 
        self.rect.left = (Settings.width - self.rect.width) // 2    # um es einfach Positionieren zu können
        self.rect.top = (Settings.height - self.rect.height) // 2
        self.speed = 3
        self.space = False


    def update(self):
        # Steuerung mit Pfeiltasten
        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
           self.rect.left -= self.speed

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            self.rect.left += self.speed

        if pygame.key.get_pressed()[pygame.K_UP] == True:
           self.rect.top -= self.speed

        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
            self.rect.top += self.speed

        # Teleportation beim loslassen der Leertaste
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            self.space = True
        if pygame.key.get_pressed()[pygame.K_SPACE] == False and self.space == True:
            self.rect.top = random.randrange(0, Settings.height - self.rect.height)
            self.rect.left = random.randrange(0, Settings.width - self.rect.width)
            self.space = False
         

        # Kollision mit dem Rand
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Settings.width:
            self.rect.right = Settings.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= Settings.height:
            self.rect.bottom = Settings.height


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.done = False

        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        self.all_racer = pygame.sprite.Group()  # Erstellt die Gruppe für die Rennautos
        self.racer1 = Racer(pygame)             # Erschafft das erste Rennauto
        self.all_racer.add(self.racer1)         # Fügt das erste Rennauto der Gruppe hinzu


    def run(self):
        while not self.done:                    # Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(Settings.fps)       # Setzt die Taktrate auf max 60fps   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Wenn das rechts obere X im Fenster geklickt
                    self.done = True

            self.screen.blit(self.background, self.background_rect)

            self.all_racer.update()             # Update Funtion für die Steuerung
            self.all_racer.draw(self.screen)    # Zeichnung des Autos


            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()               # Bereitet die Module zur Verwendung vor  
    game = Game()
    game.run()
    pygame.quit()               # beendet pygame
