import pygame
from globals import *
from sprite import Entity
from texturedata import solo_texture_data, atlas_texture_data

class Scene():
    def __init__(self, app) -> None:
        self.app = app

        self.solo_textures = self.gen_solo_textures()
        self.atlas_textures = self.gen_atlas_textures('res/atlas.png')

        self.sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.entity = Entity([self.sprites],image=self.atlas_textures['grass'])
        Entity([self.sprites],position=(100,100), image=self.solo_textures['player_static'])
        Entity([self.sprites],position=(200,200), image=self.atlas_textures['stone'])

        self.gen_world()

    def gen_solo_textures(self) -> dict:
        textures = {}

        for  name, data in solo_texture_data.items():
            textures[name] = pygame.transform.scale(pygame.image.load(data['file_path']).convert_alpha(),(data['size']))
    
        return textures
    def gen_atlas_textures(self,filepath):
        textures = {}
        atlas_img = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),(TILESIZE*16,TILESIZE*16))
    
        for name,data in atlas_texture_data.items():
            textures[name] = pygame.Surface.subsurface(atlas_img, pygame.Rect(data['position'][0]*TILESIZE, 
                                                                              data['position'][1]*TILESIZE, 
                                                                              data['size'][0],
                                                                              data['size'][1]))
        return textures
    def gen_world(self):
        pass
    def update(self):
        self.sprites.update()
    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.app.screen)