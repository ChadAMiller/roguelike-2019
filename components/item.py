from components.component import Component

class Item(Component):
    def __init__(self, use_function=None, targeting=False, targeting_message=None, targeting_radius=None, **kwargs):
        super().__init__('item')
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.targeting_radius = targeting_radius
        kwargs['targeting_radius'] = targeting_radius # this allows the spells to see their own radius while also leaving it available to the renderer
        self.function_kwargs = kwargs
