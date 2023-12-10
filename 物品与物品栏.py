from globals import *
from world.sprite import *

class Item:
    def __init__ (self, name: str="default", quantity: int =0) -> None:
        self.name = name
        self.quantity = quantity
    def ues(self,*args,**kwargs):
        pass
    def __str__(self):
        return f'Name:{self.name},Quantity:{self.quantity}'

class BlockItem(Item): # placeable item (block)
    def __init__(self, name: str, quantity: int =0) -> None:
        super().__init__(name, quantity)
    def use(self,player,position:tuple): # placing the block
        if self.quantity>0:
            items[self.name].use_type([player.group_list[group] for group in items[self.name].groups],player.textures[self.name],position,self.name)
            self.quantity-=1
            if self.quantity<=0:
                self.name="default"
        else:
            self.name="default"

class ItemData:
    def __init__ (self, name: str, quantity: int = 1, groups: list[str] = ['sprites', 'block_group'],use_type:Entity,item_type:Item=Item) -> None:
        self.name = name
        self.quantity=quantity
        self.groups = groups
        self.use_type = use_type
        self.item_type = item_type

items: dict[str,ItemData]={
    'grass':ItemData('grass',item_type=BlockItem),
    'dirt':ItemData('dirt',item_type=BlockItem),
    'stone':ItemData('stone',item_type=BlockItem),
}










from globals import *
from world.items import *
from events import EventHandler

class Inventory:
    def __init__(self, app) -> None:
        self.app = app
        self.screen = app.screen

        # create our slots
        self.slots = []
        for index in range(s):
            self.slots.append(Item())
        self.slots[1] = Blockitem( 'grass'，5)
        self.slots[2] = Blockitem( 'dirt'， 3)

        self.active_slot = 0
    def debug(self):
        for slot in self.slots:
            print(slot)
    def use(self, player, position):
        if self.slots[self.active_slot].name != "default":
            self.slots[self.active_slot].use(player, position)
    def add_item(self, item):
        first_available_slot = len(self.slots) # first empty slot
        target_slot = len(self.slots) # first slot of same name
        for index, slot in enumerate(self.slots):
            if slot.name == "default" and index < first_available_slot:
                first_available_slot = index
            if slot.name == item.name :
                target_slot =index
        if target_slot<len(self.slots):
            self.slots[target_slot].quantity+=items[item.name].quantity
        elif first_available_slot<len(self.slots):
            self.slots[first_available_slot] = items[item.name].item_type(item.name,items[item.name].quantity)
    def update(self):
        if EventHandler.keydown(pygame .K_RIGHT): # moving right in slots
            if self.active_slot < len(self.slots)-1:
                self.active_slot += 1
        if EventHandler.keydown(pygame.K LEFT): # moving left in slots
            if self.active_slot > 0:
                self.active_slot -= 1
        if EventHandler.clicked_any():
            self.debug()
    def draw(self):
        pass
