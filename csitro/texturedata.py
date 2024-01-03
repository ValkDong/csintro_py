from globals import *

atlas_texture_data = {
    'grass':{'type':'block','file_path':'res/Grass.png','size':(TILESIZE,TILESIZE),'position':(0,0)},
    'dirt':{'type':'block','file_path':'res/Dirt.png','size':(TILESIZE,TILESIZE),'position':(0,0)},
    'stone':{'type':'block','file_path':'res/Stone.png','size':(TILESIZE,TILESIZE),'position':(0,0)}
}
solo_texture_data = {
    'player_static':{'type':'player','file_path':'res/Player.png','size':(TILESIZE / 1.77 * 4,TILESIZE * 4)},
    'zombie_static':{'type':'enemy','file_path':'res/Zombie.png','size':(TILESIZE / 1.35 * 4,TILESIZE * 4)},
    'short_sword':{'type':'weapon','file_path':'res/Shortsword.png','size':(TILESIZE,TILESIZE)},
}