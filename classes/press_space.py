from arcade import draw_text
from vars import SCREEN_WIDTH

""" Skriv ut "press "space" to show menus" """


class PressSpace:
    def __init__(self, x=SCREEN_WIDTH/2, y=50):
        self.x = x
        self.y = y
        self.tick = 0
        self.timer = 0
        self.enabled = False

    def update_text(self):
        # Öka timer varje sekund
        if self.tick % 60 == 0 and self.show_text():
            self.timer += 1
        self.tick += 1

        # Sudda ut efter fyra sekunder
        if self.timer >= 4:
            self.enabled = False

        if self.show_text():
            self.enabled = True
            self.timer = 0

    def show_text(self):
        self.enabled = True

    def draw(self):
        if self.enabled:
            draw_text("Press Space to show menues", self.x, self.y, (0, 0, 0), font_size=12, width=10, align="left", anchor_x="center", anchor_y="center")
