import tcod as libtcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of the "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)
    
def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'SEEKER OF THE CHALICE')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER, 'By Xhad (for r/roguelikedev does the roguelike tutorial, 2019)')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = [
                # 'Constitution (+20 HP, from {0}'.format(player.fighter.max_hp),
                'Strength (+1 attack, from {0})'.format(player.fighter.power),
                'Agility (+1 defense, from {0}'.format(player.fighter.defense),
            ]
    menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    character_sheet = ['Character Information',
                        'Level: {0}'.format(player.level.current_level),
                        'Experience: {0}'.format(player.level.current_xp),
                        'Experience to Level: {0}'.format(player.level.experience_to_next_level),
                        'Maximum HP: {0}'.format(player.fighter.max_hp),
                        'Attack: {0}'.format(player.fighter.power),
                        'Defense: {0}'.format(player.fighter.defense),                        
                    ]
    if player.status_effects.active_statuses:
        character_sheet.append("Active Status Effects:")
        character_sheet.extend("{} ({} turns left)".format(name, status.duration) for name, status in player.status_effects.active_statuses.items())

    for i, s in enumerate(character_sheet):
        libtcod.console_print_rect_ex(window, 0, i, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, s)

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)

def win_screen(con, screen_width, screen_height):
    ending_message = '''
You have recovered the chalice and escaped the dungeon!
You win!
(press ESC to return to the main menu)
'''
    message_width = max(len(line) for line in ending_message.splitlines())
    message_box(con, ending_message, message_width, screen_width, screen_height)
