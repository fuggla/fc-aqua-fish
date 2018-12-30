import arcade, random, math
from vars import FISH_EGG_SCALING_CARROT, SCREEN_HEIGHT, SAND_RATIO, TICK_RATE


class FishEggSprite(arcade.Sprite):
    # Klass för äggen
    def __init__(self, fish):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        self.texture_egg1 = arcade.load_texture("images/egg1.png", scale=FISH_EGG_SCALING_CARROT)
        self.texture = self.texture_egg1

        # Placera ut ägget
        self.center_x = fish.center_x
        self.center_y = fish.center_y

        # Definiera variabler
        self.change_x = 0
        self.change_y = 0
        self.acc_right = 0
        self.acc_left = 0
        self.acc_grav_float = 0                 # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0

        self.sand_position = random.randint(int(self.sh * self.sr / 2), int(self.sh * self.sr))

        self.framerate = TICK_RATE
        # äggets egenskaper
        self.size = 1
        self.mass = 0.5


    def update(self):
        # Beräkna acceleration i x-led
        self.acc_right = 0
        self.acc_left = 0

        # Beräkna acceleration i y-led
        self.acc_grav_float = - 1
        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        if self.center_y < self.sand_position:
            self.acc_grav_float = 0

        # Beräkna hastighet i x-led och y-led
        else:
            self.change_x = self.change_x + (self.acc_right - self.acc_left) / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        # Anropa huvudklassen
        super().update()
