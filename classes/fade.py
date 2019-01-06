from vars import SCREEN_HEIGHT, SCREEN_WIDTH
from arcade.draw_commands import draw_xywh_rectangle_filled

# Hantering av game state
class Fade():

    def __init__(self, r=0, g=0, b=0, a=0, target_alpha=255, time = 1,
    pause=0.5):
        # Position och storlek
        self.x = 0
        self.y = 0
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT

        # Color vi vill nå innan vi går tillbaka till transparent
        self.target_alpha = target_alpha
        self.r = r
        self.g = g
        self.b = b

        # Nuvarande alpha
        self.a = a

        # ~Sekunder för fade (mediokert pga att färg inte stödjer float)
        self.time = time
        self.pause_target = pause
        self.pause_time = 0

        # Vänta på startkommando
        self.fade = "wait"

    # Starta intoning
    def start_in(self):
        self.fade = "in"
        self.a = self.target_alpha

    # Start uttoning
    def start_out(self):
        self.pause_time = 0
        self.fade = "out"
        self.a = 0

    def start(self):
        self.start_out()

    # Tona ut
    def fade_out(self, step):
        self.a += step
        if (self.a > self.target_alpha):
            self.fade = "in"
            self.a = self.target_alpha

    # Tona in
    def fade_in(self, step):
        self.a -= step
        if (self.a < 0):
            self.a = 0
            self.fade = "wait"

    # Fadea in eller ut om vi inte är i "wait"
    def update(self, dt):
        if (self.pause_time < self.pause_target):
            self.pause_time += dt
        elif not (self.fade == "wait"):
            step = int(dt * 255 / self.time)
            if (step == 0):
                step = 1
            if (self.fade == "out"):
                self.fade_out(step)
            elif (self.fade == "in"):
                self.fade_in(step)

    def draw(self):
        # Rita inte i onödan när alpha är 0
        if (self.a != 0):
            draw_xywh_rectangle_filled(self.x, self.y, self.w, self.h, (self.r, self.g, self.b, self.a))
