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
from arcade import create_text, render_text, draw_rectangle_filled, draw_rectangle_outline, draw_text, color

class Window(Shape):
    def __init__(self, x, y, w, h, title, title_height=30, title_align="center", title_background_color=(255,182,193), font_size=14, outline_size=2, outline_color=(0,0,0,128), background_color=(211,211,211)):
        super().__init__(x, y, w, h)

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
        self.calculate_edge(x, y)

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
            x = self.left + self.w / 2,
            y = self.top + self.title_height / 2,
            h = self.title_height,
            w = self.w,
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
            h = self.title_height,
            w = self.title_height,
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
        return self.visible

    # Returnera true om fönstret är stängt
    def is_closed(self):
        return not self.visible

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
            draw_rectangle_filled(*self.drop_shadow)
            draw_rectangle_filled(self.x, self.y, self.w, self.h, self.background_color)
            draw_rectangle_outline(self.x, self.y, self.w, self.h, self.outline_color, self.outline_size)
            for button in self.button_list:
                button.draw()
            for t in self.text_list:
                render_text(t.text, t.x, t.y)

    # Lägg till knapp i fönster
    def add_button(self, margin_top, margin_left, w, h, text, font_size, release):
        self.button_list.append(Button(
            x = self.left + margin_left + w / 2,
            y = self.top - margin_top - h / 2,
            w = w,
            h = h,
            outline_color = color.BLACK,
            background_color = color.GRAY,
            text = text,
            font_size = font_size,
            release = release
        ))

    # Lägg till text i fönster
    # Returnerar textrutan. Använd object.put("ny rad")
    def add_text(self, margin_top, margin_left, w, h, text=""):
        new_text = Text(
            x = self.left + margin_left,
            y = self.top - margin_top,
            w = w,
            h = h,
            text = text
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

    def calculate_shadow(self):
        self.drop_shadow=(self.x + 5, self.y - 5 + self.title_height / 2, self.w, self.h + self.title_height, (0, 0, 0, 64))

    # Flytta fönster relativt
    def move(self, x, y):
        # Flytta fönster
        self.x += x
        self.y += y

        # Räkna ut kanternas nya position
        self.calculate_edge(self.x, self.y)

        # Flytta skugga, knappar och text
        self.calculate_shadow()
        for b in self.button_list:
            b.move(x, y)
        for t in self.text_list:
            t.move(x, y)


# Rektanglulära knappar
class Button(Shape):
    def __init__(self, x, y, w, h, text, release=None, press=None, outline_size=2, outline_color=(0,0,0,128), background_color=(200,200,200), font_size=11, align="center"):
        super().__init__(x, y, w, h)

        # Text
        self.text = text
        self.font_size = font_size
        self.align = align

        # Bakgrund och ram
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.background_color = background_color

        # Funktioner som triggas vid musklick
        self.release = release or self.release
        self.press = press or self.press

    # Rita knapp
    def draw(self):
        draw_rectangle_filled(self.x, self.y, self.w, self.h, self.background_color)
        draw_rectangle_outline(self.x, self.y, self.w, self.h, self.outline_color, self.outline_size)
        draw_text(self.text, self.x, self.y, color.BLACK, font_size=self.font_size, width=self.w, align=self.align, anchor_x="center", anchor_y="center")

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
    def __init__(self, x, y, w, h, text="", font_size=8, lines=7, color=(0,0,0), align="left"):
        Shape.__init__(self, x, y, w, h)

        # Nuvarande rader
        self.message = []

        # Maximalt antal rader
        self.lines = lines

        # Text
        self.font_size = font_size
        self.color = color
        self.align = align

        # Förbered för rendering
        self.text = create_text(text, color, font_size, w, align)

    # Rita text
    def draw(self):
        render_text(self.text, self.x, self.y)

    def update(self):
        if not self.empty():
            text = ""
            while not self.empty():
                self.message.insert(0, self.get())
            i = 0
            for m in self.message:
                text = m + "\n" + text
                i += 1
                if (i == self.lines):
                    break
            self.set_text(text)

    def set_text(self, text):
        self.text = create_text(text, self.color, self.font_size, self.w, self.align)
