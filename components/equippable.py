from components.component import Component
from components.item import Item

class Equippable(Component):
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        super().__init__('equippable')
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

    def add_to_entity(self, entity):
        super().add_to_entity(entity)

        if not entity.try_component('item'):
            item = Item()
            item.add_to_entity(entity)
