import arcade
from classes.window import Window
#from classes.button import *

class Menu(Window):

    def __init__(self, x, y, width, height, title):
        super().__init__(x, y, width, height, title)

    # Lägg till knapp i meny
    def add_button(self, button):
        self.button_list.append(Button(x - 10 + width / 2, y - 10 + width / 2, 20, 20, "X", 20, self.close))
