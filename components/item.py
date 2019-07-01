from components.component import Component

class Item(Component):
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        super().__init__('item')
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
        