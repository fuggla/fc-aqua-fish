# Klass för att skapa rektangulära knappar
import arcade

class Button():

    def __init__(self, x, y, width, height, outline_size, outline_color, background_color, text, font_size, release):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.background_color = background_color
        self.text = text
        self.font_size = font_size
        self.release = release

    # Rita knapp
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, self.outline_size)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=self.font_size, width=self.width, align="center", anchor_x="center", anchor_y="center")

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
