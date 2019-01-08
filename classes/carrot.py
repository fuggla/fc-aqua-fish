import arcade,random,math
from vars import SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO, TICK_RATE, carrot_food_value


class CarrotSprite(arcade.Sprite):
    # Klass för morötter
    def __init__(self, setspeed_y=None):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        self.type = "carrot"

        img = f"assets/images/food/carrot"
        self.texture_food1 = arcade.load_texture(f"{img}/carrot1.png", scale=SPRITE_SCALING_CARROT)
        self.texture_food2 = arcade.load_texture(f"{img}/carrot2.png", scale=SPRITE_SCALING_CARROT)
        self.texture_food3 = arcade.load_texture(f"{img}/carrot3.png", scale=SPRITE_SCALING_CARROT)
        self.texture_food4 = arcade.load_texture(f"{img}/carrot4.png", scale=SPRITE_SCALING_CARROT)
        self.texture = self.texture_food1

        # Placera ut moroten
        self.center_x = random.randrange(int(self.sw * 0.8)) + int(self.sw * 0.1)
        self.center_y = self.sh

        # Definiera variabler
        self.change_x = 0
        self.change_y = setspeed_y or 0
        self.acc_x = 0
        self.acc_grav_float = 0                 # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0

        self.food_value = carrot_food_value     # Hur mycket mat finns på moroten

        self.sand_position = random.randint(int(self.sh * self.sr / 2), int(self.sh * self.sr))
        self.bounce_number = 1

        # För förflyttning med muspekaren
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

        if self.center_y < self.sh * self.sr:
            self.change_y *= 0.9
            self.change_x *= 0.9
        else:
            self.change_x = self.change_x + self.acc_x / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        # Anropa huvudklassen
        super().update()

    def drag_sprite(self, x, y, dx, dy):
        self.center_x = x
        self.center_y = y
        self.drag_speed = [dx, dy]

    def is_mouse_on(self, pointer):
        if arcade.check_for_collision(self, pointer):
            return True

    def eaten(self):
        self.food_value -= 1
        if self.food_value == 0:
            self.kill()
