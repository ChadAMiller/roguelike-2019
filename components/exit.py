from components.component import Component
from game_messages import Message

class Exit(Component):
    def __init__(self, destination=tuple(), new_floor=None): 
        super().__init__('exit')
        # destination defaults to the empty tuple because we want a falsy, immutable, ordered container
        # if a destination isn't given here, the new floor will have to be defined some other way
        self.destination = destination
        # Sets the destination now if a new floor was provided
        self.new_floor = new_floor

    def take_exit(self, player, message_log):
        # This is here for subclasses to override if they want to add logic before moving to the next room
        # e.g. the default game's healing before progressing to a new floor
        return self.next_floor

    @property
    def next_floor(self):
        if not self.new_floor:
            # construct the new floor if it doesn't exist yet
            # currently just letting this throw an exception if no destination was ever defined
            floor_constructor, args, kwargs = self.destination
            self.new_floor = floor_constructor(*args, **kwargs)

        return self.new_floor

class DownStairsExit(Exit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.already_taken = False

    def take_exit(self, player, message_log):
        if not self.already_taken:
            self.already_taken = True
            player.fighter.heal(player.fighter.max_hp // 2)
            message_log.add_message(Message('You take a moment to rest, and recover your strength.'))

        return super().take_exit(player, message_log)
