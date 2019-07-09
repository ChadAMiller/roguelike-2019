import tcod as libtcod

import components.ai as ai

from components.fighter import Fighter
from entity import Entity
from render_functions import RenderOrder

class Monster(Entity):
    def __init__(self, x, y, char, color, name, blocks=True, render_order=RenderOrder.ACTOR):
        super().__init__(x, y, char, color, name, blocks, render_order)

    def set_corpse(self):
        self.char = '%'
        self.color = libtcod.dark_red
        self.blocks = False
        self.fighter = None
        self.ai = None
        self.name = 'remains of ' + self.name
        self.render_order = RenderOrder.CORPSE

class Orc(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=20, defense=0, power=4, xp=35).add_to_entity(self)        
        ai.BasicMonster().add_to_entity(self)

class Troll(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=30, defense=2, power=8, xp=100).add_to_entity(self)
        ai.BasicMonster().add_to_entity(self)

class Balrog(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 'B', libtcod.dark_flame, 'Balrog', blocks=True, render_order=RenderOrder.ACTOR)

        Fighter(hp=45, defense=4, power=12, xp=250).add_to_entity(self)
        ai.BasicMonster().add_to_entity(self)

class Wraith(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 'w', libtcod.han, 'Wraith', blocks=False, render_order=RenderOrder.ACTOR)

        # currently player doesn't get XP for a monster that kills itself like the wraith usually does
        Fighter(hp=1, defense=0, power=0, xp=50).add_to_entity(self)
        ai.WraithMonster().add_to_entity(self)

    def set_corpse(self):
        self.blocks = False
        self.fighter = None
        self.ai = None
        self.name = ''
        self.render_order = RenderOrder.INVISIBLE

class Snake(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 's', libtcod.dark_green, 'Snake', blocks=True, render_order=RenderOrder.ACTOR)

        # It has no power because it poisons you. Poison effect is in the AI.
        Fighter(hp=20, defense=0, power=0, xp=50).add_to_entity(self)
        ai.SnakeMonster().add_to_entity(self)
