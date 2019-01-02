from arcade import draw_text
from vars import SCREEN_HEIGHT

# Beräkna FPS från delta
class Fps():
    def __init__(self, x=10, y=SCREEN_HEIGHT - 10):
        self.x = x
        self.y = y
        self.tick = 0
        self.delta_count = 0
        self.fps = 0
        self.enabled = False

    def calculate(self, dt):
        if self.enabled:
            self.tick += 1
            self.delta_count += dt
            if self.delta_count >= 1:
                self.fps = self.tick
                self.delta_count = 0
                self.tick = 0
        return self.fps

    def toggle(self):
        self.enabled = not self.enabled

    def draw(self):
        if self.enabled:
            draw_text(str(self.fps), 10, SCREEN_HEIGHT - 10, (255, 0, 0), font_size=8, width=10, align="left", anchor_x="center", anchor_y="center")
