import tcod as libtcod

import components.exit # doesn't alias to exit because of builtin exit function
from entity import Entity
from render_functions import RenderOrder

class DownStairs(Entity):
    def __init__(self, x, y, destination):
        super().__init__(x, y, '>', libtcod.white, 'Stairs (Down)', render_order=RenderOrder.STAIRS)
        components.exit.DownStairsExit(destination).add_to_entity(self)

class UpStairs(Entity):
    def __init__(self, x, y, old_floor):
        super().__init__(x, y, '<', libtcod.white, 'Stairs (Up)', render_order=RenderOrder.STAIRS)
        components.exit.UpStairsExit(new_floor=old_floor).add_to_entity(self)

class Altar(Entity):
    '''Does not use exit component because it cannot be used normally. Game winning logic is in the Chalice item instead.'''
    def __init__(self, x, y):
        super().__init__(x, y, '=', libtcod.white, 'Altar of the Dark Magician')
