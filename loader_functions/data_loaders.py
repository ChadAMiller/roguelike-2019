import os
import shelve
import dbm

def save_game(player, world, message_log, game_state):
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = world.current_floor.entities.index(player)
        data_file['world'] = world
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state

def load_game():
    try:
        with shelve.open('savegame', 'r') as data_file:        
            player_index = data_file['player_index']
            world = data_file['world']
            message_log = data_file['message_log']
            game_state = data_file['game_state']
    except dbm.error:
        raise FileNotFoundError

    player = world.current_floor.entities[player_index]

    return player, world, message_log, game_state
