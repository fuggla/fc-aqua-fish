# Klass för att skapa rektangulära knappar
import arcade
from classes.shape import Shape

class Button(Shape):

    def __init__(self, x, y, width, height, text, release=None, press=None, outline_size=2, outline_color=(0,0,0,128), background_color=(200,200,200), font_size=11):
        super().__init__(x, y, width, height)

        # Text
        self.text = text
        self.font_size = font_size

        # Bakgrund och ram
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.background_color = background_color

        # Funktioner som triggas vid musklick
        self.release = release or self.release
        self.press = press or self.press

    # Rita knapp
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, self.outline_size)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=self.font_size, width=self.width, align="center", anchor_x="center", anchor_y="center")

    def release(self):
        return True

    def press(self):
        return True

    # Kolla om angiven x y är inom knappens ramar
    # self.x och self.y är mitten av knappen
    def is_mouse_on_button(self, x, y):
        if (self.x + self.width / 2) > x > (self.x - self.width / 2) and (self.y + self.height / 2) > y > (self.y - self.height / 2):
            return True
        else:
            return False

    def on_mouse_release(self, x, y):
        if self.is_mouse_on_button(x, y):
            self.release()

    def on_mouse_press(self, x, y):
        if self.is_mouse_on_button(x, y):
            self.press()
