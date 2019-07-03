import tcod as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from render_functions import RenderOrder

class Orc(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=20, defense=0, power=4, xp=35).add_to_entity(self)        
        BasicMonster().add_to_entity(self)

class Troll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=30, defense=2, power=8, xp=100).add_to_entity(self)
        BasicMonster().add_to_entity(self)

class Balrog(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'B', libtcod.dark_flame, 'Balrog', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=45, defense=4, power=12, xp=250).add_to_entity(self)
        BasicMonster().add_to_entity(self)
