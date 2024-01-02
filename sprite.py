import pygame
from globals import *
from globals import TILESIZE
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups,image=pygame.Surface((TILESIZE,TILESIZE)),position=(0,0),namee: str = "default"):
        super().__init__(groups)
        print(name)
        self.name = name
        self.in_groups = groups
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
    def update(self):
        pass

class Mob(Entity):
    def __init__(self,groups,image=pygame.Surface((TILESIZE, TILESIZE)), position=(0,0),parameters = {}):
        super().__init__(groups,image,position)

        if parameters:
            self.block_group = parameters['block_group']
            self.player = parameters['player']
            self.damage = parameters['damage']

        self.velocity=pygame.math.Vector2()
        self.mass=5
        self.speed=0.5
        self.terminal_velocity = TERMINALVELOCITY*self.mass

        #states
        self.attacking=True
        self.grounded=False
        
        self.attacking = True
        self.attacked = False
        self.grounded = False
        
def move(self):
    self.velocity.y += GRAVITY * self.mass

    if self.velocity.y > self.terminal_velocity:
        self.velocity.y = self.terminal_velocity

    if abs(math.sqrt((self.rect.x-self.player.rect.x)**2+(self.rect.y-self.player.rect.y)**2)) < TILESIZE*10:
        if self.rect.x > self.player.rect.x:
            self.velocity.x = -self.speed
        elif self.rect.x < self.player.rect.x:
            self.velocity.x = self.speed
        self.attacking = True
    else:
        self.attacking = False
        self.velocity.x = 0
        
    self.rect.x += self.velocity.x * PLAYERSPEED
    self.check_collisions('horizontal')
    self.rect.y += self.velocity.y 
    self.check_collisions('vertical')

    if self.grounded and self.attacking and abs(self.velocity.x) < 0.1:
        self.velocity.y = -8
def check_collisions(self,direction):
    if direction == "horizontal":
        for block in self.block_group:
            if block.rect.colliderect(self.rect):
                if self.velocity.x > 0:
                    self.rect.right = block.rect.left
                if self.velocity.x < 0:
                    self.rect.left = block.rect.right

                self.veocity.x=0
    elif direction=="vertical":
        collisions = 0
        for block in self.block_group:
            if block.rect.colliderect(self.rect):
                if self.velocity.y > 0:
                    collisions += 1
                    self.rect.bottom = block.rect.top
                if self.velocity.y < 0:
                    self.rect.top = block.rect.bottom
        if collisions > 0:
            self.grounded = True
        else:
            self.grounded = False
def check_player_collision(self):
    if self.attacking and not self.attacked:
        if self.rect.colliderect(self.player.rect):
            self.player.health -= self.damage
            self.attacked = True
            self.counter = self.attack_cooldown

            if self.player.rect.x > self.rect.centerx:
                self.player.velocity.x = 3
            elif self.player.rect.x < self.rect.centerx:
                self.player.velocity.x = -3
def update(self):
    self.move()
    self.check_player_collision()

    if self.attacked:
        self.counter -= 1
        if self.counter < 0:
            self.counter = self.attack_cooldown
            self.attacked = False
