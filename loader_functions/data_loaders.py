import os
import shelve
import dbm

def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state

def load_game():
    try:
        with shelve.open('savegame', 'r') as data_file:        
            player_index = data_file['player_index']
            entities = data_file['entities']
            game_map = data_file['game_map']
            message_log = data_file['message_log']
            game_state = data_file['game_state']
    except dbm.error:
        raise FileNotFoundError

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
