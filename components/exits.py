from components.component import Component
from game_messages import Message

class Exit(Component):
    def __init__(self, destination=tuple()): 
        super().__init__('exit')
        # destination defaults to the empty tuple because we want a falsy, immutable, ordered container
        # if there isn't a value given in the constructor, a destination floor will have to be set later
        # by manually setting these parameters (may write a method for it later)
        self.destination = destination
        # new_floor is not constructed until needed, otherwise setting up a dungeon requires
        # setting up all floors and is an infinite loop unless the dungeon is finite
        self.new_floor = None

    def take_exit(self, player, message_log):
        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest, and recover your strength.'))
        return self.next_floor

    @property
    def next_floor(self):
        if not self.new_floor:
            # construct the new floor if we haven't yet
            # currently just letting this throw an exception if no destination was defined
            floor_constructor, args, kwargs = self.destination
            self.new_floor = floor_constructor(*args, **kwargs)

        return self.new_floor
