import tcod as libtcod

import components.exits as exits # yes, map_objects/exits currently imports components/exits and it sounds silly to me too
from entity import Entity
from render_functions import RenderOrder

class DownStairs(Entity):
    def __init__(self, x, y, destination):
        super().__init__(x, y, '>', libtcod.white, 'Stairs (Down)', render_order=RenderOrder.STAIRS)
        exits.DownStairsExit(destination).add_to_entity(self)

class UpStairs(Entity):
    def __init__(self, x, y, old_floor):
        super().__init__(x, y, '<', libtcod.white, 'Stairs (Up)', render_order=RenderOrder.STAIRS)
        exits.Exit(destination=(), new_floor=old_floor).add_to_entity(self)

