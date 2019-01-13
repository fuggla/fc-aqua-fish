import arcade,random,math
from vars import SPRITE_SCALING_FISH_HOOK, SCREEN_WIDTH, SCREEN_HEIGHT, TICK_RATE

class FishHookSprite(arcade.Sprite):
    # Klass för krok
    def __init__(self, hook_list):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        img = f"assets/images/fish_hook"
        self.texture_fish_hook = arcade.load_texture(f"{img}/fish_hook.png", scale=SPRITE_SCALING_FISH_HOOK)
        self.texture = self.texture_fish_hook

        # Definiera variabler
        self.change_x = 0
        self.change_y = - 50
        self.acc_x = 0
        self.acc_grav_float = 0                 # Fulvariabel, summan av gravitationen och lyftkraften
        self.acc_water_res = 0
        self.popcorn = True
        self.has_fish = False
        self.hook_list = hook_list
        self.not_placed = True
        self.try_place_number = 10
        self.active = True

        self.stop_y = int(self.sh * 0.7) + random.randrange(int(self.sh * 0.1))

        # För förflyttning med muspekaren
        self.dragged = False
        self.drag_speed = [0, 0]

        self.framerate = TICK_RATE
        # Morotens egenskaper
        self.size = 1
        self.mass = 0.5

        # Kroken placeras endast om det finns plats
        self.illegal_coordinates = []
        for hook in self.hook_list:
            coordinates = [hook.center_x - 100, hook.center_x + 100]
            self.illegal_coordinates.append(coordinates)

        while self.not_placed and self.try_place_number > 0:
            self.not_placed = False
            test_center_x = int(self.sw * 0.1) + random.randrange(int(self.sw * 0.8))
            for coordinates in self.illegal_coordinates:
                if coordinates[0] < test_center_x < coordinates[1]:
                    self.not_placed = True
                    test_center_x = - 10000
                    self.try_place_number -= 1
                    break

        self.center_x = test_center_x
        self.center_y = self.sh + 20


    def update(self):
        # Beräkna acceleration i x-led
        self.acc_x = - (self.size * self.change_x * math.fabs(self.change_x)) / self.mass

        # Beräkna acceleration i y-led
        if self.center_y < self.stop_y:
            self.acc_grav_float = 0

        else:
            self.acc_grav_float = - 1

        if not self.popcorn and not self.has_fish:
            self.acc_grav_float = 2
        elif self.has_fish:
            self.acc_grav_float = 4
            self.size = 0.5

        self.acc_water_res = (self.size * self.change_y * math.fabs(self.change_y)) / self.mass

        if self.dragged:
            self.change_x = 0
            self.change_y = 0
        else:
            self.change_x = self.change_x + self.acc_x / self.framerate
            self.change_y = self.change_y + (self.acc_grav_float - self.acc_water_res) / self.framerate

        if self.center_y > self.sh * 1.2:
            self.kill()

        # Anropa huvudklassen
        super().update()

    def no_fish(self):
        self.popcorn = False
