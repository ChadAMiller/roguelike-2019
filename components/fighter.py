import tcod as libtcod

from random import randint

from components.component import Component
from game_messages import Message

class Fighter(Component):
    def __init__(self, hp, defense, power, hit, xp=0):
        super().__init__("fighter")
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.hit = hit
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.try_component('equipment'):
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.try_component('equipment'):
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target, ignore_armor=False):
        results = []

        roll = randint(1,20)

        if roll + self.hit < target.fighter.defense:
            damage = 0
        elif ignore_armor:
            damage = self.power
        else:
            damage = self.power

        if damage > 0:
            results.append({'message': Message('{0} attacks {1}, dealing {2} damage.'.format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
