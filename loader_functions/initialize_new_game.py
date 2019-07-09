import tcod as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.status_effects import StatusEffects

from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import World
from render_functions import RenderOrder


def get_constants():
    window_title = 'Roguelike Tutorial Overhauled'

    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50),
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors,
    }

    return constants

def get_game_variables(constants):
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR)
    Fighter(hp=100, defense=2, power=2).add_to_entity(player)
    Level().add_to_entity(player)

    inventory_component = Inventory(26)
    inventory_component.add_to_entity(player)
    
    equipment_component = Equipment()
    equipment_component.add_to_entity(player)

    dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger')
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    equippable_component.add_to_entity(dagger)    
        
    inventory_component.add_item(dagger)
    equipment_component.toggle_equip(dagger)

    StatusEffects().add_to_entity(player)
    
    world = World(player, constants['map_width'], constants['map_height'])

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, world, message_log, game_state
