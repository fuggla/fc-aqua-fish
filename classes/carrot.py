import arcade,random,math

# Klass för lila fiskar (Purple_fish)
class CarrotSprite(arcade.Sprite):
    def __init__(self, SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Anropa Sprite konstruktor
        super().__init__()

        global sw
        global sh
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        global carrot_cor
        carrot_cor = [0, 0]

        self.texture_carrot1 = arcade.load_texture("images/carrot1.png", scale=SPRITE_SCALING_CARROT)

        self.texture = self.texture_carrot1

        # Placera ut moroten
        self.center_x = random.randrange(sw * 0.8) + sw * 0.1
        self.center_y = sh

        # Definiera variabler
        self.change_x = 0
        self.change_y = 0
        self.acc_right = 0
        self.acc_left = 0
        self.acc_grav_float = 0             # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0

        self.framerate = 30         # Ska fixas sen
        # Morotens egenskaper
        self.size = 1
        self.mass = 0.1


    def update(self):
        # Updatera koordinaterna innan de skickas iväg
        global carrot_cor
        carrot_cor = self.get_position()

        # Beräkna acceleration i x-led
        self.acc_right = 0
        self.acc_left = 0

        # Beräkna acceleration i y-led
        self.acc_grav_float = - 1
        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        # Beräkna hastighet i x-led och y-led
        self.change_x = self.change_x + (self.acc_right - self.acc_left) / self.framerate
        self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate


        # Anropa huvudklassen
        super().update()

    def get_coordinates(self):
        # Metod som skickar iväg morotens koordinater
        return carrot_cor