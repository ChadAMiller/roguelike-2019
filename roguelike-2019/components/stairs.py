from components.component import Component

class Stairs(Component):
    def __init__(self, floor):
        super().__init__('stairs')
        self.floor = floor
