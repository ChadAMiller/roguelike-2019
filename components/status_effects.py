from components.component import Component

from game_messages import Message

class StatusEffect(Component):
    def __init__(self, status_name, effect, duration):
        super().__init__('status_effect')
        self.status_name = status_name
        self.effect = effect
        self.duration = duration

class StatusEffects(Component):
    def __init__(self):
        super().__init__('status_effects')
        self.active_statuses = {}

    def add_status(self, status):
        # Current stacking rules are that adding another status of the same name resets the duration. They don't stack, so you can't be 'double poisoned'
        self.active_statuses[status.status_name] = status

    def process_statuses(self):

        results = []

        to_delete = set()
        for name, status in self.active_statuses.items():
            if status.duration == 0:
                to_delete.add(name)
            else:
                status.duration -= 1
                results.extend(status.effect(self.owner))

        for name in to_delete:
            del self.active_statuses[name]
            results.append({'message': Message("{0} wore off.".format(name))})

        return results

class HealOverTime(StatusEffect):
    def __init__(self, status_name, amount, duration):
        self.amount = amount
        def effect(target):
            target.fighter.heal(amount)
            return []

        super().__init__(status_name, effect, duration)

    def __getstate__(self):
        # This getstate/setstate business is so that the effect can be incorporated in a save game. Don't know how I'll generalize this yet.
        return {'status_name': self.status_name, 'amount': self.amount, 'duration': self.duration}

    def __setstate__(self, state):
        self.__init__(state['status_name'], state['amount'], state['duration'])
        
class DamageOverTime(StatusEffect):
    def __init__(self, status_name, amount, duration):
        self.amount = amount
        def effect(target):
            # unlike healing, take_damage returns results
            return target.fighter.take_damage(amount)
        
        super().__init__(status_name, effect, duration)

    def __getstate__(self):
        return {'status_name': self.status_name, 'amount': self.amount, 'duration': self.duration}

    def __setstate__(self, state):
        self.__init__(state['status_name'], state['amount'], state['duration'])