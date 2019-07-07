import tcod as libtcod

import item_functions

from components.equippable import Equippable
from components.item import Item
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import Message
from render_functions import RenderOrder

class HealingPotion(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.heal, amount=40).add_to_entity(self)

class RejuvenationPotion(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '!', libtcod.desaturated_blue, "Potion of Rejuvenation", render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.regenerate, name="Potion of Rejuvenation", amount=10, duration=4).add_to_entity(self)

class Sword(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '/', libtcod.sky, 'Sword')
        Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3).add_to_entity(self)

class Shield(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '[', libtcod.orange, 'Shield')
        Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1).add_to_entity(self)

class FireballScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3).add_to_entity(self)

class LightningScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_lightning, damage=40, maximum_range=5).add_to_entity(self)

class ConfusionScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_confuse, targeting=True, targeting_message=Message('Left-click and enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)).add_to_entity(self)
