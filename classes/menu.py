import arcade
from classes.window import Window
from classes.button import Button
#from classes.button import *

class Menu(Window):

    def __init__(self, x, y, width, height, title):
        super().__init__(x, y, width, height, title)

    # Lägg till knapp i meny
    def add_button(self, x, y, width, height, text, font_size, function):
        self.button_list.append(Button(
            self.x + x,
            self.y + y,
            width,
            height,
            text,
            font_size,
            function
        ))
