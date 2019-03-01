from arcade import draw_text
from vars import SCREEN_WIDTH,SCREEN_HEIGHT

""" Skriv ut "press "Q" to exit" """


class PressQ:
    def __init__(self, x=SCREEN_WIDTH-50, y=30):
        self.x = x
        self.y = y
        self.tick = 0
        self.timer = 0
        self.enabled = False

    def update_text(self):
        # Öka timer varje sekund
        if self.tick % 60 == 0:
            self.timer += 1
        self.tick += 1

        # Visa efter fyra sekunder
        if self.timer >= 90:
            self.show_text()

    def show_text(self):
        self.enabled = True

    def hide_text(self):
        self.enabled = False
        self.timer = 0

    def draw(self):
        if self.enabled:
            draw_text("Press Q to Exit", self.x, self.y, (60, 60, 90), font_size=12, width=100, align="center", anchor_x="center", anchor_y="center")
