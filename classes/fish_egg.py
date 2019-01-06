import arcade, random, math
from vars import SCALING_FISH_EGG, SCREEN_HEIGHT, SAND_RATIO, TICK_RATE, fish_egg_hatch_age, fish_egg_disapear_age


class FishEggSprite(arcade.Sprite):
    # Klass för äggen
    def __init__(self, fish, size):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        if size == "large":
            self.scale_factor = SCALING_FISH_EGG * 3
        elif size == "medium":
            self.scale_factor = SCALING_FISH_EGG * 2
        else:
            self.scale_factor = SCALING_FISH_EGG

        img = "assets/images/egg"
        self.texture_egg1 = arcade.load_texture(f"{img}/egg1.png", scale=self.scale_factor)
        self.texture_egg_cracked = arcade.load_texture(f"{img}/egg_cracked.png", scale=self.scale_factor)
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
        self.origin = fish.type
        self.age = 0
        self.hatch_age = fish_egg_hatch_age
        self.disapear_age = fish_egg_disapear_age

        self.sand_position = random.randint(int(self.sh * self.sr / 2), int(self.sh * self.sr))

        self.framerate = TICK_RATE
        # äggets egenskaper
        self.size = 1
        self.mass = 1


    def update(self):
        # Beräkna acceleration i x-led
        self.acc_right = 0
        self.acc_left = 0

        # Beräkna acceleration i y-led
        self.acc_grav_float = - 1
        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        # Beräkna hastighet i x-led och y-led
        if self.center_y > self.sand_position:
            self.change_x = self.change_x + (self.acc_right - self.acc_left) / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        elif self.center_y < self.sand_position and self.change_y < 0:
            self.change_y += 1
        else:
            self.change_x = 0
            self.change_y = 0

        # Anropa huvudklassen
        super().update()
