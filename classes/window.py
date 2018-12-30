"""
Klass för att visa ett fönster

+------------------+---+
|       TITEL      | X |
+------------------+---+
|                      |
| +------------------+ |
| |      Knapp 1     | |
| +------------------+ |
|                      |
| +------------------+ |
| |      Knapp 2     | |
| +------------------+ |
|                      |
+----------------------+
"""

import arcade
from classes.button import Button
from classes.shape import Shape

class Window(Shape):

    def __init__(self, x, y, width, height, title, title_height=30, title_align="center", title_background_color=(255,182,193), font_size=14, outline_size=2, outline_color=(0,0,0,128), background_color=(211,211,211)):
        super().__init__(x, y, width, height)

        # Ram och bakgrund
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

        # Skugga bakom fönstret
        self.drop_shadow=(self.x + 5, self.y - 5 + self.title_height / 2, self.width, self.height + self.title_height, (0, 0, 0, 64))

        # Avgör om fönstret är synligt
        self.visible = False

        # Avgör om fönstret flyttas
        self.dragging = False

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
            align = title_align,
            release = self.stop_dragging,
            press = self.start_dragging
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

    # Öpnna eller stäng fönster
    def toggle(self):
        self.visible = not self.visible

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

    # Kolla om det har klickats på en knapp i fönstret
    def on_mouse_press(self, x, y):
        for b in self.button_list:
            b.on_mouse_press(x, y)

    # Rita fönster
    def draw(self):
        if self.is_open():
            arcade.draw_rectangle_filled(*self.drop_shadow)
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

    def update_buttons(self, x, y):
        for b in self.button_list:
            b.set_position(x, y)

    def stop_dragging(self):
        self.dragging = False

    def start_dragging(self):
        self.dragging = True

    def is_dragged(self):
         return True if self.dragging else False

    # Flytta fönster relativt
    def move(self, x, y):
        # Flytta fönster
        self.x += x
        self.y += y

        # Flytta skugga
        self.drop_shadow=(self.x + 5, self.y - 5 + self.title_height / 2, self.width, self.height + self.title_height, (0, 0, 0, 64))

        # Rökna ut kanternas nya position
        self.left = x - self.width / 2
        self.top = y + self.height / 2
        self.bottom = y - self.height / 2
        self.right = x + self.width / 2

        # Flytta knappar
        for b in self.button_list:
            b.move(x, y)
