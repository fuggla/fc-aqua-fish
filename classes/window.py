# Klass för att visa fönster
import arcade
from classes.button import Button

class Window():

    def __init__(self, x, y, width, height, title, title_height=30, title_background_color=(255,182,193), font_size=14, outline_size=2, outline_color=(0,0,0,128), background_color=(211,211,211)):

        # Position, storlekt och färg
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.background_color = background_color

        # Text längst upp på fönstret
        self.title = title
        self.title_height = title_height
        self.title_background_color = title_background_color
        self.font_size = font_size

        # Fönstrets kanter
        self.left = x - width / 2
        self.top = y + height / 2
        self.bottom = y - height / 2
        self.right = x + width / 2

        # Avgör om fönstret är synligt
        self.visible = True

        # Fönstret innehåller knappar
        self.button_list = []

        # Stor ram längst upp på fönstret fungerar som en knapp
        self.button_list.append(Button(
            x = self.left + self.width / 2,
            y = self.top + self.title_height / 2,
            height = self.title_height,
            width = self.width,
            outline_size = self.outline_size,
            background_color = title_background_color,
            text = title,
            font_size = self.font_size,
            release = self.is_open
        ))

        # En X knapp i höger hörn för att stänga fönstret
        self.button_list.append(Button(
            x = self.right - self.title_height / 2,
            y = self.top + self.title_height / 2,
            height = self.title_height,
            width = self.title_height,
            outline_size = self.outline_size,
            outline_color = (0, 0, 0, 0),
            background_color = (100, 0, 0, 100),
            text = "X",
            font_size = self.title_height - 10,
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
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.background_color)
            arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, self.outline_size)
            for button in self.button_list:
                button.draw()

    # Lägg till knapp i fönster
    def add_button(self, margin_top, margin_left, width, height, text, font_size, release):
        self.button_list.append(Button(
            x = self.left + margin_left + width / 2,
            y = self.top - margin_top - height / 2,
            width = width,
            height = height,
            outline_color = arcade.color.BLACK,
            background_color = arcade.color.GRAY,
            text = text,
            font_size = font_size,
            release = release
        ))
