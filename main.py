import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
    
        self.running =True

    def run(self):
        while self.running:
            self.update()
            self.draw()
        self.close()
    def update(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running =False

        pygame.display.update()
    def draw(self):
        self.scene.fill('lightblue')
    def close(self):
        pygame.quit()
        sys.exit()

if __name__=="__main__":
    game = Game()
    game.run()
