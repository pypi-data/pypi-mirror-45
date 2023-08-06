from . import sprite_canvas
# import sprite_code


class Sprite:
    def __init__(self, project):
        self.project = project

        costumes = [
            {"file":"106798711d0220a08cca12e750468e2b.png", "name":"costume1"}, 
            {"file":"27a0bf89451a32a7eea1930e3e2bfce4.png", "name":"12"}
        ]
        self.sprite_canvas = sprite_canvas.SpriteCanvas(
            project,                       # project
            project.canvas_object,         # canvas object
            "Sprite1",                     # name
            1,                             # layer order
            True,                          # visible
            0,                             # x
            0,                             # y
            100,                           # size
            90,                            # direction
            False,                         # draggable
            "all around",                  # rotate style
            costumes,                      # list of costumes
            0                              # current costume
        )

        

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            function_name = name
            function_arguements = args
            self.add_instruction_to_queue(function_name, function_arguements)
        return wrapper



    def add_instruction_to_queue(self, block, parameters):
        item_function = getattr(self.sprite_canvas, block)
        item = {
            'function': item_function,
            'parameters': parameters
        }
        self.project.queue.put(item)