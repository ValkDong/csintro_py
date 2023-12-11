import pygame
from globals import *
from events import EventHandler
from world.sprite import Entity

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, parameters: dict) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)

        self.textures = parameters['textures']
        self.group_list = parameters['group list']
        self.block_group = self.group_list['block_group']
        self.enemy_group = self.group_list['enemy_group']
        self.inventory = parameters['inventory']

        self.health = parameters['health']
        
        self.velocity = pygame.math.Vector2()
        self .mass = 5
        self.terminal)_velocity = self.mass * TERMINALVELOCITY

        self.grounded = True
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = 1
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if not keys[pygame .K a] and not keys[pygame .K d]:
            if self.velocity.x > 0:
                self.velocity.x -= 0.1
            elif self.velocity.x < 0:
                self.velocity.x += 0.1

            if abs(self.velocity.x)<0.3:
                self.velocity.x = 0

        if self.grounded and EventHandler .keydown(pygame .K_SPACE):
            self.velocity.y = -PLAYERJUMPPOWER

        if EventHandler.clicked(1):
            for enemy in selfenemy_group:
                if enemy.rect.colliderect(self.get adjusted mouse position()):
                    self.inventory.slots[self.inventory.active slot].attack(self, enemy)
    def move(self):
        self.velocity.x += GRAVITY + self.mass
