"""
Klass för att visa ett fönster med knappar och text

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
| +------------------+ |
| |      Textruta    | |
| +------------------+ |
|                      |
+----------------------+
"""

from classes.shape import Shape
from queue import SimpleQueue
from arcade import create_text, render_text, draw_rectangle_filled, draw_rectangle_outline, draw_text, draw_lrtb_rectangle_filled
from arcade.color import *

class Window(Shape):
    def __init__(self, x, y, w, h, title, title_height=30, title_align="center", title_bg_color=(255,182,193), font_size=13, font_name="Arial", outline_size=2, outline_color=(0,0,0,128), bg_color=(211,211,211)):
        super().__init__(x, y, w, h)

        # Ram och bakgrund
        self.outline = [outline_color, outline_size]
        self.bg_color = bg_color

        # Text längst upp på fönstret
        self.title = title
        self.title_height = title_height
        self.title_bg_color = title_bg_color
        self.font_size = font_size
        self.font_name = font_name

        # Fönstrets kanter
        self.lrtb = self.calculate_edge(*self.pos)

        # Skugga bakom fönstret
        self.calculate_shadow()

        # Avgör om fönstret är synligt
        self.visible = False

        # Avgör om fönstret flyttas
        self.dragging = False

        # Fönstret innehåller knappar och text
        self.button_list = []
        self.text_list = []

        # Stor ram längst upp på fönstret fungerar som en knapp
        self.button_list.append(Button(
            x = self.left + w / 2,
            y = self.top + title_height / 2,
            h = title_height,
            w = w,
            outline_size = outline_size,
            bg_color = title_bg_color,
            text = title,
            font_size = font_size,
            font_name = font_name,
            align = title_align,
            release = self.stop_dragging,
            press = self.start_dragging
        ))

        # En X knapp i höger hörn för att stänga fönstret
        self.button_list.append(Button(
            x = self.right - title_height / 2,
            y = self.top + title_height / 2,
            h = title_height,
            w = title_height,
            outline_size = outline_size,
            outline_color = BLACK,
            bg_color = (100, 0, 0, 100),
            text = "X",
            font_size = title_height - 10,
            font_name = font_name,
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
        return self.visible

    # Returnera true om fönstret är stängt
    def is_closed(self):
        return not self.visible

    # Returnera lista på alla knappar
    def get_buttons(self):
        return self.button_list

    # Kolla om det har klickats på en knapp i fönstret
    def on_mouse_release(self, *pos):
        for b in self.button_list:
            b.on_mouse_release(*pos)

    # Kolla om det har klickats på en knapp i fönstret
    def on_mouse_press(self, *pos):
        for b in self.button_list:
            b.on_mouse_press(*pos)

    # Rita fönster
    def draw(self):
        if self.is_open():
            draw_rectangle_filled(*self.drop_shadow)
            draw_lrtb_rectangle_filled(*self.lrtb, self.bg_color)
            draw_rectangle_outline(*self.pos, *self.size, *self.outline)
            for button in self.button_list:
                button.draw()
            for t in self.text_list:
                t.draw()

    # Lägg till knapp i fönster
    def add_button(self, text, release, margin_top, margin_left, w, h,
    font_size=11, outline_color=BLACK, bg_color=GRAY, font_name="Arial",
    font_color=BLACK):
        self.button_list.append(Button(
            x = self.left + margin_left + w / 2,
            y = self.top - margin_top - h / 2,
            w = w,
            h = h,
            outline_color = outline_color,
            bg_color = bg_color,
            text = text,
            font_size = font_size,
            font_name = font_name,
            font_color = font_color,
            release = release
        ))

    # Lägg till flera knappar samtidigt i fönster
    def add_buttons(self, settings, *buttons):
        for button in buttons:
            self.add_button(*button, *settings)

    # Lägg till text i fönster
    # Returnerar textrutan. Använd object.put("ny rad")
    def add_text(self, margin_top, margin_left, w, h, text="", rows=7, align="left"):
        new_text = Text(
            x = self.left + margin_left,
            y = self.top - margin_top,
            w = w,
            h = h,
            text = text,
            rows = rows,
            align = align
        )
        self.text_list.append(new_text)
        return new_text

    def update_buttons(self, x, y):
        for b in self.button_list:
            b.set_position(x, y)

    def stop_dragging(self):
        self.dragging = False

    def start_dragging(self):
        self.dragging = True

    def is_dragged(self):
         return self.dragging

    def calculate_edge(self, x, y):
        self.left = x - self.w / 2
        self.top = y + self.h / 2
        self.bottom = y - self.h / 2
        self.right = x + self.w / 2
        return [self.left, self.right, self.top, self.bottom]

    def calculate_shadow(self):
        self.drop_shadow=(self.x + 5, self.y - 5 + self.title_height / 2, self.w, self.h + self.title_height, (0, 0, 0, 64))

    # Flytta fönster relativt
    def move(self, dx, dy):
        # Flytta fönster
        self.x += dx
        self.y += dy
        self.pos = [self.x, self.y]

        # Räkna ut kanternas nya position
        self.lrtb = self.calculate_edge(*self.pos)

        # Flytta skugga, knappar och text
        self.calculate_shadow()
        for b in self.button_list:
            b.move(dx, dy)
        for t in self.text_list:
            t.move(dx, dy)


# Rektanglulära knappar
class Button(Shape):
    def __init__(self, x, y, w, h, text, release=None, press=None,
    outline_size=2, outline_color=(0,0,0,128), bg_color=(200,200,200),
    font_size=11, font_name="Calibri", align="center", font_color = BLACK):
        super().__init__(x, y, w, h)

        # Text
        self.text = text
        self.font_size = font_size
        self.align = align
        self.font_name = font_name
        self.font_color = font_color

        # Bakgrund och ram
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.bg_color = bg_color

        # Funktioner som triggas vid musklick
        self.release = release or self.release
        self.press = press or self.press

    # Rita knapp
    def draw(self):
        draw_rectangle_filled(self.x, self.y, self.w, self.h, self.bg_color)
        draw_rectangle_outline(self.x, self.y, self.w, self.h, self.outline_color, self.outline_size)
        draw_text(self.text, self.x, self.y, self.font_color, font_name=self.font_name, font_size=self.font_size, width=self.w, align=self.align, anchor_x="center", anchor_y="center")

    def release(self):
        return True

    def press(self):
        return True

    # Kolla om angiven x y är inom knappens ramar
    # self.x och self.y är mitten av knappen
    def is_mouse_on_button(self, x, y):
        if (self.x + self.w/ 2) > x > (self.x - self.w/ 2) and (self.y + self.h/ 2) > y > (self.y - self.h/ 2):
            return True
        else:
            return False

    def on_mouse_release(self, x, y):
        if self.is_mouse_on_button(x, y):
            self.release()

    def on_mouse_press(self, x, y):
        if self.is_mouse_on_button(x, y):
            self.press()

# Textrutor med ett begränsat antal rader
class Text(Shape, SimpleQueue):
    def __init__(self, x, y, w, h, text="", font_size=8, rows=7, color=(0,0,0), align="left"):
        Shape.__init__(self, x, y, w, h)

        # Max och nuvarande rader
        self.max_rows = rows
        self.row = []

        # Förbered för rendering
        self.settings = [color, font_size, w, align]
        self.text = create_text(text, *self.settings)

    # Rita text
    def draw(self):
        render_text(self.text, self.x, self.y)

    def message_received(self):
        return not self.empty()

    # Töm kö och fyll på textruta med ny rad
    def update(self):
        text = ""
        self.row.insert(0, self.get())
        for r in self.row[0:self.max_rows]:
            text = f"{r}\n{text}"
        self.text = create_text(text, *self.settings)
