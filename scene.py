from opensimplex import OpenSimplex
from camera import Camera
from inventory.inventory import Inventory

class Scene:
    def _init_(self,app) -> None:
        self.app=app

        self.textures=self.gen_solo_textures()
        self.textures=update(self.gen_atlas_textures('res/owatlas.png'))

        self.sprites=Camera()
        self.blocks=pygame.sprite.Group()
        self.group_list:dict[str,pygame.sprite.Group]={
            'sprites':self.sprites,
            'block_group':self.blocks
        }

        self.inventory=Inventory(self.app,self.atlas_textures)

        self.entity=Entity([self.sprites],image=self.atlas_textures['grass'])
        Entity([self.sprites],position=(200,200),image=self.atlas_textures['stone'])

        Entity([self.sprites,self.blocks],pygame.Surface((TILESIZE*10,TILESIZE)),position=(400,550))

        self.player = Player([self.sprites],self.textures['player_static'],(600,300),parameters={
