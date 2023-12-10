import pygame
from globals import *
from world.sprite import Entity,Mob
from world.player import Player
from world.texturedata import solo_texture_data, atlas_texture_data
from opensimplex import OpenSimplex
from camera import Camera
from inventory.inventory import Inventory
from world.items import *

class Scene():
    def __init__(self, app) -> None:
        self.app = app

        self.textures = self.gen_solo_textures()
        self.textures.updata(self.gen_atlas_textures('res/owatlas.png'))

        self.sprites = Camera()
        self.blocks = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.group_list: dict[str, pygame.sprite.Group()]={
            'sprites':self.sprites,
            'block_group':self.blocks,
            'enemy_group':self.enemy_group
        }

        # invetory
        self.inventory =Inventory(self.app, self.textures)

        self.entity = Entity([self.sprites],image=self.textures['grass'])
        Entity([self.sprites],position=(200,200), image=self.textures['stone'])

        #floor
        Entity([self.sprites, self.blocks], pygame.Surface((TILESIZE*10,TILESIZE)),position=(400,550))

        self.player = Player([self.sprites], self.textures['player_static'],(600,300),parameters={
                                                            'textures':self.textures,
                                                            'group_list':self.group_list,
                                                            'inventory':self.inventory,
                                                            'health':3})
        
        # Entity
        Mob([self.sprites, self.enemy_group], self.textures['zombie_static'],(800.-500),parameters={'block_group':self.blocks,
                                                                                                   'player':self.player,
                                                                                                   'damage':1})
        
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
        noise_generator =OpenSimplex(seed=92392893)

        heightmap=[]
        for y in range (6000):
            noise_value =noise_generator.noise2(y *0.05,0)
            height = int((noise_value +1)*4+5)
            heightmap.append(height)
        
        for x in range (len(heightmap)):
            for y in range(heightmap[x]):
                y_offset =5-y +6
                block_type = 'dirt'
                if y== heightmap[x]-1:
                    block_type='grass'
                if y<heightmap[x]-5:
                    block_type='stone'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x*TILESIZE,y_offset*TILESIZE),name =block_type)

    def update(self):
        self.sprites.update()
        self.inventory.updata()
    def draw(self):
        self.app.screen.fill('lightblue')
        self.inventory.draw()

        self.sprites.draw(self.player, self.app.screen)

class Chunk:
    CHUNKSIZE = 30
    CHUNKPIXELSIZE = CHUNKSIZE * TILESIZE

    def __init__(self,
                 position: tuple[int ,int],
                 group_list:dict[str,pygame.sprite.Group],
                 textures:dict[str,pygame.Surface]) -> None:
        self.position = position
        self.group_list = group_list
        self.textures = textures

        self.blocks: list[Entity] = []
    def gen_chunk(self):
        noise_generator =OpenSimplex(seed=92392893)

        heightmap=[]
        for y in range (Chunk.CHUNKSIZE * self.position[0], Chunk.CHUNKSIZE * self.position[0] + Chunk.CHUNKSIZE):
            noise_value =noise_generator.noise2(y *0.05,0)
            height = int((noise_value +1)*4+5)
            heightmap.append(height)
        
        for x in range (len(heightmap)):
            for y in range(heightmap[x]):
                y_offset =5-y +6
                block_type = 'dirt'
                if y== heightmap[x]-1:
                    block_type='grass'
                if y<heightmap[x]-5:
                    block_type='stone'
                

    def load_chunk(self):
        pass
    def unload_chunk(self):
        pass