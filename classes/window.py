# Klass för att visa fönster
import arcade
from classes.button import Button

class Window():

    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.left = x - width / 2
        self.top = y + height / 2
        self.bottom = y - height / 2
        self.right = x + width / 2
        self.title = title
        self.bar_height = 30
        self.font_size = 14
        self.visible = True
        self.button_list = []

        # Kant längst upp på fönstret
        self.button_list.append(Button(
            x = self.left + self.width / 2,
            y = self.top + self.bar_height / 2,
            height = self.bar_height,
            width = self.width,
            outline_size = 2,
            outline_color = arcade.color.RED,
            background_color = arcade.color.PINK,
            text = "",
            font_size = 20,
            release = self.is_open
        ))

        # En X knapp i höger hörn för att stänga fönstret
        self.button_list.append(Button(
            x = self.right - self.bar_height / 2,
            y = self.top + self.bar_height / 2,
            height = self.bar_height,
            width = self.bar_height,
            outline_size = 2,
            outline_color = arcade.color.RED,
            background_color = arcade.color.PINK,
            text = "X",
            font_size = 20,
            release = self.close
        ))

    # Öppna fönster
    def open(self):
        self.visible = True

    # Stäng fönster
    def close(self):
        self.visible = False

    # Returnera true om fönstret är öppet
    def is_open(self):
        return True if self.visible else False

    # Returnera true om fönstret är stängt
    def is_closed(self):
        return False if self.visible else True

    # Returnera lista på alla knappar
    def get_buttons(self):
        return self.button_list

    # Kolla om det har klickats på en knapp i fönstret
    def on_mouse_release(self, x, y):
        for b in self.button_list:
            b.on_mouse_release(x, y)

    # Rita fönster
    def draw(self):
        if self.is_open():
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.LIGHT_GRAY)
            for button in self.button_list:
                button.draw()

    # Lägg till knapp i fönster
    def add_button(self, margin_top, margin_left, width, height, text, font_size, release):
        self.button_list.append(Button(
            x = self.left + margin_left + width / 2,
            y = self.top - margin_top - height / 2,
            width = width,
            height = height,
            outline_size = 2,
            outline_color = arcade.color.BLACK,
            background_color = arcade.color.GRAY,
            text = text,
            font_size = font_size,
            release = release
        ))
