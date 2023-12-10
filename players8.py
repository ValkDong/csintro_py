def block_handling(self):
    placed=False
    collision=False
    mouse_pos=self.get_adjusted_mouse_position()
    
    if EventHandler.clicked_any():
        for block in self.block_group:
            if block.rect.collidepoint(mouse_pos):
                collision=True
                if EventHandler.clicked(1):
                    bolck.kill()
            if EventHandler.clicked(3):
                if not coiilsion:
                    placed=True
    if placed and not collision:
        Entity(block.in_groups,self.textures['grass'],self.get_block_pos(mouse_pos))                   
def get_adjusted_mouse_position(self) -> tuple:
    mouse_pos = pygame.mouse.get_pos()

    player_offset = pygame.math.Vector2()
    player_offset.x = SCREENWIDTH / 2 - self.rect.centerx
    player_offset.y = SCREENHEIGHT / 2 - self.rect.centery

    return (mouse_pos[0] - player_offset.x, mouse_pos[1] - player_offset.y)
def get_block_pos(self,mouse_pos:tuple):
    return (int((mouse_pos[0]//TILESIZE)*TILESIZE),int((mouse_pos[1]//TILESIZE)*TILESIZE))
def update(self):
    self.input()
    self.move()
self.block_handling()
