import pygame                   # Stellt Objekte und Konstanten zur Spielprogrammierung zur Verfügung
import os
import random
import time

class Settings(object):
    width = 400
    height = 700
    fps = 60
    title = "Game_1_3 Geisterfahrer"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")
    score = 0
    enemys = 0
    counter = 0
    try:
        f = open("highscore.json", "r")
        highscore = f.readline()
        f.close()
    except:
        f = open("highscore.json", "w")
        f.write(str(0))
        f.close()
        highscore = 0

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

class Racer(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "racer01.png")).convert_alpha() # Bild wird mit Alphakanal geladen
        self.image = pygame.transform.scale(self.image, (40, 75))
        self.rect = self.image.get_rect()                           # Setzt ein Rechteck um das Auto
        self.rect.left = (Settings.width - self.rect.width) // 2
        self.rect.top = (Settings.height - self.rect.height) - 50
        self.speed = 3
        self.space = False


    def update(self):
        # Steuerung mit Pfeiltasten
        if pygame.key.get_pressed()[pygame.K_LEFT] == True or pygame.key.get_pressed()[pygame.K_a]:
           self.rect.left -= self.speed

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True or pygame.key.get_pressed()[pygame.K_d]:
            self.rect.left += self.speed

        if pygame.key.get_pressed()[pygame.K_UP] == True or pygame.key.get_pressed()[pygame.K_w]:
           self.rect.top -= self.speed

        if pygame.key.get_pressed()[pygame.K_DOWN] == True or pygame.key.get_pressed()[pygame.K_s]:
            self.rect.top += self.speed
         

        # Kollision mit dem Rand
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Settings.width:
            self.rect.right = Settings.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= Settings.height:
            self.rect.bottom = Settings.height

        # Verlangsamung auf dem Gras
        if self.rect.left <= 25 or self.rect.right >= Settings.width - 25:
            self.speed = 1
        else:
            self.speed = 3

    def teleport(self):
        self.rect.top = random.randrange(0, Settings.height - self.rect.height)
        self.rect.left = random.randrange(0, Settings.width - self.rect.width)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "enemy01.png")).convert_alpha() # Bild wird mit Alphakanal geladen
        self.image = pygame.transform.scale(self.image, (40, 75))
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(48, 313)      # Gegner spawnen nur auf der Fahrbahn
        self.rect.bottom = random.randrange(-1000, 0)
        if Settings.score < 25:
            self.speed = 2
        if Settings.score >= 25 < 50:
            self.speed = 3
        if Settings.score >= 50 < 75:
            self.speed = 4
        if Settings.score >= 75 < 100:
            self.speed = 5
        if Settings.score >= 150:
            self.speed = 6


    def update(self):
        self.rect.top += self.speed
        if self.rect.top >= Settings.height:
            Settings.score += 1
            Settings.enemys -= 1
            self.kill()
        


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.done = False
        self.space = False

        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        self.all_racer = pygame.sprite.Group()  # Erstellt die Gruppe für die Rennautos
        self.racer = Racer(pygame)             # Erschafft das erste Rennauto
        self.all_racer.add(self.racer)         # Fügt das erste Rennauto der Gruppe hinzu

        self.all_enemy = pygame.sprite.Group()
        self.end = False


        pygame.font.init()
        self.endfont = pygame.font.SysFont('Arial', 50)
        self.font = pygame.font.SysFont('Arial', 22)
        
        self.gameover = self.endfont.render('Gameover', False, (0, 0, 0))

        self.screenscore = self.font.render('Score: ' + str(Settings.score), False, (0, 0, 0))
        self.screenhighscore = self.font.render('Highscore: ' + str(Settings.highscore), False, (0, 0, 0))
        
        self.score = self.endfont.render('Score: ' + str(Settings.score), False, (0, 0, 0))
        self.highscore = self.endfont.render('Highscore: ' + str(Settings.highscore), False, (0, 0, 0))
        

    def run(self):
        while not self.done:                    # Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(Settings.fps)       # Setzt die Taktrate auf max 60fps   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Wenn das rechts obere X im Fenster geklickt
                    self.done = True

            self.screen.blit(self.background, self.background_rect)

            if self.end == False:
                self.all_racer.update()             # Update Funtion für die Steuerung
                self.all_racer.draw(self.screen)

                if Settings.score < 25:
                    Settings.counter = 3
                if Settings.score >= 25 < 50:
                    Settings.counter = 4
                if Settings.score >= 50 < 75:
                    Settings.counter = 5
                if Settings.score >= 75 < 100:
                    Settings.counter = 6
                if Settings.score >= 150:
                    Settings.counter = 7

                while Settings.enemys <= Settings.counter:
                    self.enemy = Enemy(pygame)
                    self.all_enemy.add(self.enemy)
                    Settings.enemys += 1

                self.all_enemy.draw(self.screen)
                self.all_enemy.update()

                if pygame.key.get_pressed()[pygame.K_SPACE] == True:
                    self.space = True
                if pygame.key.get_pressed()[pygame.K_SPACE] == False and self.space == True:
                    while True:
                        self.racer.teleport()
                        collision = pygame.sprite.spritecollide(self.racer, self.all_enemy, False)
                        if collision != True:
                            self.racer.rect.top += 150
                            collision = pygame.sprite.spritecollide(self.racer, self.all_enemy, False)
                            if collision != True:
                                break
                    self.space = False
                self.all_racer.draw(self.screen)

                self.screenscore = self.font.render('Score: ' + str(Settings.score), False, (0, 0, 0))
                self.screenhighscore = self.font.render('Latest Highscore: ' + str(Settings.highscore), False, (0, 0, 0))
                
                self.score = self.endfont.render('Score: ' + str(Settings.score), False, (0, 0, 0))
                self.highscore = self.endfont.render('Latest Highscore: ' + str(Settings.highscore), False, (0, 0, 0))

                self.screen.blit(self.screenscore,(0,22))
                self.screen.blit(self.screenhighscore,(0,0))

                collision = pygame.sprite.spritecollide(self.racer, self.all_enemy, False)
                if collision:
                    self.end = True
                    time.sleep(1)
                    if Settings.score > int(Settings.highscore):
                        f = open("highscore.json", "w")
                        f.write(str(Settings.score))
                        f.close()

            if self.end == True:
                self.screen.blit(self.gameover,(100,200))
                
                self.screen.blit(self.score,(100,270))
                self.screen.blit(self.highscore,(0,320))
            
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()               # Bereitet die Module zur Verwendung vor  
    game = Game()
    game.run()
    pygame.quit()               # beendet pygame
