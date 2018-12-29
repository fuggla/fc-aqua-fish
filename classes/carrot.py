import arcade,random,math
from vars import SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO, carrot_food_value

# Klass för lila fiskar (Purple_fish)
class CarrotSprite(arcade.Sprite):
    def __init__(self):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        self.texture_carrot1 = arcade.load_texture("images/carrot1.png", scale=SPRITE_SCALING_CARROT)
        self.texture = self.texture_carrot1

        # Placera ut moroten
        self.center_x = random.randrange(int(self.sw * 0.8)) + int(self.sw * 0.1)
        self.center_y = self.sh

        # Definiera variabler
        self.change_x = 0
        self.change_y = 0
        self.acc_right = 0
        self.acc_left = 0
        self.acc_grav_float = 0                 # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0

        self.food_value = carrot_food_value     # Hur mycket mat finns på moroten

        self.sand_position = random.randint(int(self.sh * self.sr / 2), int(self.sh * self.sr))
        self.bounce_number = 1

        self.framerate = 30         # Ska fixas sen
        # Morotens egenskaper
        self.size = 1
        self.mass = 0.5


    def update(self):
        # Beräkna acceleration i x-led
        self.acc_right = 0
        self.acc_left = 0

        # Beräkna acceleration i y-led
        self.acc_grav_float = - 1
        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        if self.center_y < self.sand_position and self.bounce_number <= 5:
            self.acc_grav_float = 100 / self.bounce_number
            self.bounce_number += 1

        # Beräkna hastighet i x-led och y-led
        if self.bounce_number > 5:
            self.change_y = 0
            self.change_x = 0
        else:
            self.change_x = self.change_x + (self.acc_right - self.acc_left) / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        # Anropa huvudklassen
        super().update()

    def eaten(self):
        self.food_value -= 1
        if self.food_value == 0:
            self.kill()