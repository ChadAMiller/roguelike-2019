import tcod as libtcod
from random import randint

from entity import Entity
from game_messages import Message
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder

import map_objects.exits as exits
import map_objects.items as items
import map_objects.monsters as monsters

from map_objects.rectangle import Rect
from map_objects.tile import Tile

DEFAULTS = {
    'room_max_size': 10,
    'room_min_size': 6,
    'max_rooms': 30,
}

DUNGEON_DEPTH = 10 # Not entirely happy with this, still thinking about it

def get_or_default(d, k):
    return d.get(k, DEFAULTS[k])

class World:
    def __init__(self, player, map_width, map_height):
        self.current_floor = StartingFloor(player, map_width, map_height)

    def change_room(self, player, entity, message_log):
        # remember the player's current position in case they come back to this room
        self.current_floor.last_player_position = (player.x, player.y)

        self.current_floor = entity.exit.take_exit(player, message_log)

        # reset the player's position if they've been here before
        # note: currently this does not work if a player has more than one way to reenter a room where they've already been
        if self.current_floor.last_player_position:
            player.x, player.y = self.current_floor.last_player_position

class DungeonFloor:
    def __init__(self, player, map_width, map_height, dungeon_level, **kwargs):

        # This could be turned into a for loop but not without confusing the linter
        self.room_max_size = get_or_default(kwargs, 'room_max_size')
        self.room_min_size = get_or_default(kwargs, 'room_min_size')
        self.max_rooms = get_or_default(kwargs, 'max_rooms')
        self.previous_floor = kwargs.get('previous_floor', None)
        self.name = kwargs.get('name', "Dungeon Floor: {}".format(dungeon_level))

        self.entities = [player]
        self.width = map_width
        self.height = map_height
        self.dungeon_level = dungeon_level
        self.initialize_tiles()
        self.make_map(player)

        # To handle the case where the player reenters a floor from an upward staircase
        self.last_player_position = None

    def make_map(self, player):
        '''This should be overridden by subclasses'''
        raise NotImplementedError

    def initialize_tiles(self):
        self.tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked

    def find_exit(self):
        '''For the snake AI. Currently the last exit in the list is the downward stairs'''
        return [e for e in self.entities if e.try_component('exit')][-1]

    def find_entity(self, condition, key=None):
        entities_list = sorted((e for e in self.entities if condition(e)), key=key)
        return entities_list[0] if entities_list else None

class StandardFloor(DungeonFloor):
    def make_map(self, player):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for _ in range(self.max_rooms):
            # random width and height
            w = randint(self.room_min_size, self.room_max_size)
            h = randint(self.room_min_size, self.room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # 'paint' it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts
                    player.x = new_x
                    player.y = new_y
                    if self.previous_floor:
                        self.entities.append(exits.UpStairs(new_x, new_y, self.previous_floor))
                else:
                    # all rooms after the first
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        if self.dungeon_level < DUNGEON_DEPTH:
            destination=(
                StandardFloor,
                (player, self.width, self.height, self.dungeon_level + 1),
                {'room_max_size': self.room_max_size, 'room_min_size': self.room_min_size, 'max_rooms': self.max_rooms, 'previous_floor': self})
        else:
            destination=(
                EndingFloor,
                (player, self.width, self.height, self.dungeon_level + 1),
                {'previous_floor': self})
        self.entities.append(exits.DownStairs(center_of_last_room_x, center_of_last_room_y, destination))

    def place_entities(self, room):
        # Get a random number of monsters
        max_monsters_per_room = from_dungeon_level([[2,1],[3,4],[5,6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1,1],[2,4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
                        monsters.Orc: 80,
                        monsters.Archer: from_dungeon_level([(i*2, i) for i in range(DUNGEON_DEPTH)], self.dungeon_level),
                        monsters.Snake: from_dungeon_level([(i*10, i) for i in range(DUNGEON_DEPTH)], self.dungeon_level),
                        monsters.Troll: from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level),
                        monsters.Balrog: from_dungeon_level([(max(i-4*10, i), i) for i in range (DUNGEON_DEPTH)], self.dungeon_level),
                        monsters.Wraith: from_dungeon_level([(i, i) for i in range(10)], self.dungeon_level),
                        }

        item_chances = {}

        sword_chances = {items.sword_class(i+2): from_dungeon_level([[i*2, i]], self.dungeon_level) for i in range(DUNGEON_DEPTH)}
        item_chances.update(sword_chances)

        shield_chances = {items.shield_class(i): from_dungeon_level([[i*3, i]], self.dungeon_level) for i in range(DUNGEON_DEPTH)}
        item_chances.update(shield_chances)

        potion_chances = {
                        items.HealingPotion: 5,
                        items.RejuvenationPotion: 35,
                        }
        item_chances.update(potion_chances)

        scroll_chances = {
                        items.LightningScroll: from_dungeon_level([[25, 4]], self.dungeon_level),
                        items.FireballScroll: from_dungeon_level([[25, 6]], self.dungeon_level),
                        items.ConfusionScroll: from_dungeon_level([[10, 2]], self.dungeon_level),
                        }
        item_chances.update(scroll_chances)

        for _ in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in self.entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                self.entities.append(monster_choice(x, y))

        for _ in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in self.entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                self.entities.append(item_choice(x, y))

class StartingFloor(DungeonFloor):
    def __init__(self, player, map_width, map_height):
        super().__init__(player, map_width, map_height, 0, name="Entry Chamber")

    def make_map(self, player):
        starting_room = Rect(self.width // 2, self.height // 2, 6, 10)
        center = starting_room.center()
        self.create_room(starting_room)

        player.x, player.y = center
        player.y += 3

        self.entities.append(exits.Altar(player.x, player.y))

        destination=(
            StandardFloor,
            (player, self.width, self.height, self.dungeon_level + 1),
            {'room_max_size': self.room_max_size, 'room_min_size': self.room_min_size, 'max_rooms': self.max_rooms, 'previous_floor': self})
        self.entities.append(exits.DownStairs(center[0], center[1]-3, destination))

class EndingFloor(DungeonFloor):
    def __init__(self, player, map_width, map_height, dungeon_level, **kwargs):
        super().__init__(player, map_width, map_height, dungeon_level, name="Hall of the Chalice", **kwargs)

    def make_map(self, player):
        ending_room = Rect(self.width // 2, self.height // 2, 6, 10)
        center = ending_room.center()
        self.create_room(ending_room)

        player.x, player.y = center
        player.y += 3

        self.entities.append(exits.UpStairs(player.x, player.y, self.previous_floor))
        self.entities.append(items.Chalice(center[0], center[1]-3))
