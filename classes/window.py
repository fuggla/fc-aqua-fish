# Klass för att skapa rektangulära knappar
import arcade
from classes.button import Button

class Window():

    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.title = title
        self.font_size = 14
        self.button_list = []
        self.open = True
        self.button_list.append(Button(x - 10 + width / 2, y - 10 + width / 2, 20, 20, "X", 20, self.close))

    def close(self):
        self.open = False

    def is_open(self):
        return True if self.open else False

    def is_closed(self):
        return False if self.open else True

    def get_buttons(self):
        return self.button_list

    def on_mouse_release(self, x, y):
        for b in self.button_list:
            b.on_mouse_release(x, y)

    # Rita meny
    def draw(self):
        if self.is_open():
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.LIGHT_GRAY)
            for button in self.button_list:
                button.draw()
