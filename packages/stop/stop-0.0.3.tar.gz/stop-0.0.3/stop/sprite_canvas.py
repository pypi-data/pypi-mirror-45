import tkinter as tk
import stop.scratch_math as v
import random
from PIL import Image, ImageTk

class SpriteCanvas:
    def __init__(self, project, canvas, name, layer_order, visible, x, y, size, direction, draggable, rotation_style, costumes, current_costume):
        # self.main =             main
        self.project =          project
        self.canvas =           canvas
        self.name =             name
        self.layer_order =      layer_order         # number
        self.visible =          visible             # true / false
        self.x =                x
        self.y =                y                   
        self.size =             size                # percentage`
        self.direction =        direction           # -179 to 180 angle
        self.draggable =        draggable           # True / False
        self.rotation_style =   rotation_style      # Left-Right / Dont Rotate / All Around
        self.costumes =         costumes            # array of image names
        self.current_costume =  current_costume     # num
        # NOT BUILT INS
        # creating canvas image
        self.canvas_img = self.canvas.canvas.create_image((0, 0))
        self.pil_img = None
        self.pil_img_edited = None
        self.tk_img = None
        
        self.update_position()
        self.update_sprite()


    def move_steps(self, parameters):  # steps
        steps = parameters[0]
        x = 0
        y = 0
        if self.direction == 0:
            y = steps
        elif self.direction == 90:
            x = steps
        elif self.direction == 180:
            y = 0 - steps
        elif self.direction == -90:
            x = 0 - steps
        else:
            x = steps*v.sin(self.direction)
            y = steps*v.cos(self.direction)
        self.x += x
        self.y += y
        self.update_position()

    def turn_right_degrees(self, parameters):  # degrees
        degrees = parameters[0]
        self.direction += degrees
        self.update_sprite()

    def turn_left_degrees(self, parameters):  # degrees
        degrees = parameters[0]
        self.direction -= degrees
        self.update_sprite()

    def go_to(self, parameters):  # option
        option = parameters[0]
        if option == "random_position":
            x = random.randint(-240, 240)
            y = random.randint(-180, 180)
        elif option == "mouse_pointer":
            # use system to find mouse coordinates
            x = None
            y = None
        else:
            # use system to find other sprite coordinates
            sprite = self.main.sprites[option]
            x = sprite.x
            y = sprite.y
        self.x = x
        self.y = y
        self.update_position()

    def go_to_x_y(self, parameters):  # x, y
        self.x = parameters[0]
        self.y = parameters[1]
        self.update_position()

    def glide_secs_to(self, parameters):  # option, seconds
        option = parameters[0]
        seconds = parameters[1]
        if option == "random_position":
            x = random.randint(-240, 240)
            y = random.randint(-180, 180)
        elif option == "mouse_pointer":
            # use system to find mouse coordinates
            x = None
            y = None
        else:
            # use system to find other sprite coordinates
            x = None
            y = None
        self.x = x
        self.y = y

    def glide_secs_to_x_y(self, parameters):  # x, y
        # work - do replace 'glide' with a 'for loop + goto'
        self.x = parameters[0]
        self.y = parameters[1]

    def point_in_direction(self, parameters):  # direction
        self.direction = parameters[0]
        self.update_sprite()

    def point_towards(self, parameters):  # option
        option = parameters[0]
        if option == "mouse_pointer":
            # use system to find mouse coordinates
            target_x = None
            target_y = None
        else:
            # use system to find other sprite coordinates
            target_x = None
            target_y = None
        x = target_x - self.x
        y = target_y - self.y
        angle = (y / x).atan()
        self.direction = angle

    def change_x_by(self, parameters):  # x
        self.x += parameters[0]
        self.update_position()

    def set_x_to(self, parameters):  # x
        self.x = parameters[0]
        self.update_position()

    def change_y_by(self, parameters):  # y
        self.y += parameters[0]
        self.update_position()

    def set_y_to(self, parameters):  # y
        self.y = parameters[0]
        self.update_position()

    def if_on_edge_bounce(self, parameters): # not straightforward
        pass

    def set_rotation_style(self, parameters):  # option
        option = parameters[0]
        self.rotation_style = option

    def say_for_seconds(self, parameters): # use global function?
        pass

    def say(self, parameters):
        pass

    def think_for_seconds(self, parameters):
        pass

    def switch_costume_to(self, parameters):  # costume
        costume = parameters[0]
        if type(costume) == "int":
            self.switch_costume_to_num(costume)
        elif type(costume) == "str":
            try:
                self.switch_costume_to_str(costume)
            except ValueError:
                self.switch_costume_to_num(costume)
        self.update_sprite()


    def next_costume(self, parameters):
        self.current_costume += 1
        if self.current_costume > len(self.costumes)-1:
            self.current_costume = 0
        self.update_sprite()

    def switch_backdrop_to(self, parameters):
        pass

    def next_backdrop(self, parameters):
        pass

    def change_size_by(self, parameters):  # percentage
        percentage = parameters[0]
        new_size = (self.size + percentage, )
        # print('new_size:', new_size)
        self.set_size_to(new_size)

    def set_size_to(self, parameters):  # percentage
        # print('here:', parameters)
        percentage = parameters[0]
        self.size = percentage
        if self.size < 1:
            self.size = fv1
        self.update_sprite()

    def show(self, parameters):
        self.visible = True
        self.update_sprite()

    def hide(self, parameters):
        self.visible = False
        self.update_sprite()





    ### NOT BUILT INS ###


    def find_index_of_dictionary_in_list_with_key(self, list_of_dictionaries, key, value):
        for index, dictionary in enumerate(list_of_dictionaries):
            if dictionary[key] == value:
                return index
        raise ValueError

    def switch_costume_to_str(self, costume):
        costume_dictionary_index = self.find_index_of_dictionary_in_list_with_key(self.costumes, "name", costume)
        index = costume_dictionary_index+1
        self.current_costume = index

    def switch_costume_to_num(self, costume):
        if costume.value in range(len(self.costumes)):
            self.current_costume = costume
        else:
            self.current_costume = costume % len(self.costumes)

    def update_position(self):
        x = self.x + 240
        y = 180 - self.y
        self.canvas.canvas.coords(self.canvas_img, x, y)

    def update_size(self):
        multiplier = self.size * 0.01
        current_width = self.pil_img.size[0]
        current_height = self.pil_img.size[1]
        new_width = current_width*multiplier
        new_height = current_height*multiplier
        new_size = (int(float(new_width)), int(float(new_height)))
        self.pil_img_edited = self.pil_img.resize(new_size)

    def update_costume(self):
        self.pil_img = Image.open("assets/{0}".format(self.costumes[int(self.current_costume)-1]["file"]))


    def update_rotation(self):
        if self.rotation_style == "all around":
            self.pil_img_edited = self.pil_img_edited.rotate(int(0-self.direction)+90, expand=1, resample=Image.BICUBIC)
        elif self.rotation_style == "dont rotate":
            pass
        elif self.rotation_style == "left-right":
            if self.direction < 0:
                self.pil_img_edited = self.pil_img_edited.transpose(Image.FLIP_LEFT_RIGHT)

    def update_sprite(self):
        if self.visible:
            self.update_costume()
            self.update_size()
            self.update_rotation()
            self.tk_img = ImageTk.PhotoImage(self.pil_img_edited)
            self.canvas.canvas.itemconfig(self.canvas_img, image=self.tk_img, state="normal")
        else:
            self.canvas.canvas.itemconfig(self.canvas_img, state="hidden")
            


