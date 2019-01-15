import arcade, random, math
from vars import SPRITE_SCALING_PLANT_FOREGROUND, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO

class PlantForeground(arcade.Sprite):
    # Klass för blåbärsplantan
    def __init__(self, plant_blueberry_list):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO
        self.plant_blueberry_list = plant_blueberry_list
        self.not_placed = True

        self.textures = []
        img = "assets/images/plant"
        self.append_texture(arcade.load_texture(f"{img}/seaweed2.png", scale=SPRITE_SCALING_PLANT_FOREGROUND))
        self.append_texture(arcade.load_texture(f"{img}/seaweed2.png", mirrored=True, scale=SPRITE_SCALING_PLANT_FOREGROUND))

        # Placera ut blåbärsplantan
        self.try_place_number = 5

        if random.random() < 0.5:
            self.set_texture(0)
        else:
            self.set_texture(1)


        self.illegal_coordinates = []
        for plant in self.plant_blueberry_list:
            coordinates = [plant.center_x - 50, plant.center_x + 50]
            self.illegal_coordinates.append(coordinates)

        while self.not_placed and self.try_place_number > 0:
            self.not_placed = False
            if random.random() < 0.5:
                test_center_x = random.randrange(int(self.sw * 0.02), int(self.sw * 0.15))
            else:
                test_center_x = random.randint(int(self.sw * 0.85), int(self.sw * 0.98))
            test_center_y = random.randint(int(self.sh * self.sr * 0.5), int(self.sh * self.sr * 0.7))
            for coordinates in self.illegal_coordinates:
                if coordinates[0] < test_center_x < coordinates[1]:
                    self.not_placed = True
                    test_center_y = - 1000
                    self.try_place_number -= 1
                    break

        self.center_x = test_center_x
        self.center_y = test_center_y


    def update(self):
        pass
        # Anropa huvudklassen
        super().update()
