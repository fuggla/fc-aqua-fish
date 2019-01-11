import arcade,random,math
from vars import SPRITE_SCALING_FISH_HOOK, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO, TICK_RATE

class FishHookSprite(arcade.Sprite):
    # Klass för krok
    def __init__(self):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        img = f"assets/images/food/fish_hook"
        self.texture_fish_hook = arcade.load_texture(f"{img}/fish_hook.png", scale=SPRITE_SCALING_FISH_HOOK)
        self.texture = self.texture_fish_hook

        # Definiera variabler
        self.center_x = None
        self.center_y = None
        self.change_x = 0
        self.change_y = 0
        self.acc_x = 0
        self.acc_grav_float = 0                 # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0

        # För förflyttning med muspekaren
        self.dragged = False
        self.drag_speed = [0, 0]

        self.framerate = TICK_RATE
        # Morotens egenskaper
        self.size = 1
        self.mass = 0.5


    def update(self):
        # Beräkna acceleration i x-led
        self.acc_x = - (self.size * self.change_x * math.fabs(self.change_x)) / self.mass

        # Beräkna acceleration i y-led
        self.acc_grav_float = - 1
        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        if self.dragged:
            self.change_x = 0
            self.change_y = 0
        else:
            self.change_x = self.change_x + self.acc_x / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        # Anropa huvudklassen
        super().update()

    def drag_sprite(self, x, y, dx, dy):
        self.center_x = x
        self.center_y = y
        self.drag_speed = [dx, dy]

    def release(self):
        self.change_x = self.drag_speed[0]  # Ställ in spritens x-hastighet
        self.change_y = self.drag_speed[1]  # Ställ in spritens y-hastighet

    def is_mouse_on(self, pointer):
        if arcade.check_for_collision(self, pointer):
            return True
