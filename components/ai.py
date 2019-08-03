import tcod as libtcod

from random import randint

from components.component import Component
from game_messages import Message

from components import status_effects

class AiComponent(Component):
    def __init__(self):
        super().__init__('ai')

class BasicMonster(AiComponent):
    def take_turn(self, target, fov_map, game_map):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

class ConfusedMonster(AiComponent):
    def __init__(self, previous_ai, number_of_turns=10):
        super().__init__()
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map)

            self.number_of_turns -= 1

        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

class WraithMonster(AiComponent):
    def __init__(self):
        super().__init__()
        self.player_spotted = False

    def take_turn(self, target, fov_map, game_map):
        results = []
        monster = self.owner

        # Return without doing anything until it spots the player for the first time
        if not self.player_spotted and not libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            return results

        self.player_spotted = True
        self.owner.move_towards(target.x, target.y, game_map, ignore_blocking=True)

        if monster.distance_to(target) == 0:
            results.append({'message': Message("The wraith has haunted you!")})
            target.status_effects.add_status(status_effects.DamageOverTime('Haunted', 5, 10))
            results.extend(monster.fighter.take_damage(1))
        
        return results

class SnakeMonster(AiComponent):
    def take_turn(self, target, fov_map, game_map):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if 'Poisoned' in target.status_effects.active_statuses:
                # run for the exit if player is already poisoned, or in a random direction if path to the exit is blocked
                current_position = monster.x, monster.y
                stairs = game_map.find_exit()
                monster.move_astar(stairs, game_map, max_path=None)
                if current_position == (monster.x, monster.y):
                    monster.flee(target, game_map)
            
            elif monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.append({'message': Message("The snake has poisoned you!")})
                target.status_effects.add_status(status_effects.DamageOverTime('Poisoned', 1, 20))
                results.extend(attack_results)

        return results

class ArcherMonster(AiComponent):
    def take_turn(self, target, fov_map, game_map):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) <= 2:
                monster.flee(target, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
