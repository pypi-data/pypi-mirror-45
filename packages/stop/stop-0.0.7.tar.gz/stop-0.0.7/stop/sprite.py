from . import sprite_canvas
# import sprite_code


class Sprite:
    def __init__(self, project, costumes=False):
        self.project = project

        if not costumes:
            path = "{0}/../assets/".format(__file__)
            costumes = [
                {"file":"{0}costume1.png".format(path), "name":"costume1"}, 
                {"file":"{0}costume2.png".format(path), "name":"costume2"}
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