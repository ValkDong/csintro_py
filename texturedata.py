from globals import *

atlas_texture data = {
    'grass': {'type': 'block', 'size': (TILESIZE，TILESIZE), 'position': (0, 0)},
    'dirt': {'type': 'block', 'size': (TILESIZE.TILESIZE), 'position': (0, 1)},
    'stone': {'type': 'block', 'size': (TILESIZE，TILESIZE), 'position': (1, 0)},
}

solo texture data = {
    'player_static': {'type': 'player', 'file_path':'res/player.png', 'size': (TILESIZE * 4，TILESIZE * 4)},
    'zombie_static': {'type': 'enemy', 'file_path': 'res/zombie.png', 'size': (TILESIZE * 4，TILESIZE * 4)},
    'short_sword': {'type': 'weapon', 'file_path':'res/weapons/shortsword.png'，'size': (TILESIZE，TILESIZE)},
}
