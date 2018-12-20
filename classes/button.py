# Klass för att skapa rektangulära knappar
import arcade

class Button():

    def __init__(self, x, y, width, height, text, font_size, click):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.font_size = font_size
        self.click = click

    # Rita knapp
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.LIGHT_GRAY)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=self.font_size, width=self.width, align="center", anchor_x="center", anchor_y="center")

    # Kolla om angiven x y är inom knappens ramar
    # self.x och self.y är mitten av knappen
    def is_mouse_on_buttom(self, x, y):
        if (self.x + self.width / 2) > x > (self.x - self.width / 2) and (self.y + self.height / 2) > y > (self.y - self.height / 2):
            return True
        else:
            return False
