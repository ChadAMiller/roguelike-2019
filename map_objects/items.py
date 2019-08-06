import tcod as libtcod

from functools import partial

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
    def __init__(self, x, y, bonus=3):
        super().__init__(x, y, '/', libtcod.sky, 'Sword (+{})'.format(bonus))
        Equippable(EquipmentSlots.MAIN_HAND, power_bonus=bonus).add_to_entity(self)

class Shield(Entity):
    def __init__(self, x, y, bonus=1):
        super().__init__(x, y, '[', libtcod.orange, 'Shield (+{})'.format(bonus))
        Equippable(EquipmentSlots.OFF_HAND, defense_bonus=bonus).add_to_entity(self)

class FireballScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), targeting_radius=3, damage=25).add_to_entity(self)

    def valid_target(self, mouse, fov_map, entity):
        return libtcod.map_is_in_fov(fov_map, mouse.cx, mouse.cy) and entity.try_component('fighter')

class LightningScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_lightning, damage=40, maximum_range=5).add_to_entity(self)

class ConfusionScroll(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.cast_confuse, targeting=True, targeting_message=Message('Left-click and enemy to confuse it, or right-click to cancel.', libtcod.light_cyan), targeting_radius=0).add_to_entity(self)

    def valid_target(self, mouse, fov_map, entity):
        return libtcod.map_is_in_fov(fov_map, mouse.cx, mouse.cy) and entity.try_component('ai')

class Chalice(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'y', libtcod.violet, 'Magic Chalice', render_order=RenderOrder.ITEM)
        Item(use_function=item_functions.rub_chalice).add_to_entity(self)

def sword_class(bonus):
    return partial(Sword, bonus=bonus)

def shield_class(bonus):
    return partial(Shield, bonus=bonus)
