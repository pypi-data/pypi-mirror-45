

class spriteCode:
    def __init__(self, project, sprite, sprite_canvas):
        self.project = project
        self.sprite = sprite
        self.sprite_canvas = sprite_canvas

        # all event scripts
        self.all_methods = dir(self)

        self.when_green_flag_clicked_methods = [
            method in self.all_methods if method.startswith('green_flag_')
        ]
        self.when_key_pressed_methods = []
        self.when_this_sprite_clicked_methods = []
        self.when_backdrop_switches_to_methods = []
        self.when_greater_than_methods = []
        self.when_i_recieve_methods = []

        for method in self.all_methods:
            if method.startswith

    # EVENT HANDLERS

    def event_green_flag(self): # startswith: green_flag_
        for method in self.when_green_flag_clicked_methods:
            method()


    # CUSTOM SCRIPTS IN SPRITE

    def green_flag_1(self):
        






    # NON-SCRIPT METHODS

    def add_instruction_to_queue(self, block, parameters):
        item_function = getattr(self.sprite_canvas.move_steps, block)
        item = {
            'function': item_function,
            'parameters': parameters
        }
        this.project.queue.put(item)

    