class Component:
    def __init__(self, name):
        self.name = name

    def add_to_entity(self, entity):
        setattr(entity, self.name, self)
        self.owner = entity
