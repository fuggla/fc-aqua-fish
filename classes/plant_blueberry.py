import arcade, random, math
from vars import SPRITE_SCALING_PLANT_BLUEBERRY, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO


class PlantBlueberry(arcade.Sprite):
    # Klass för blåbärsplantan
    def __init__(self, plant_blueberry_list):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        self.has_berry = False

        self.plant_blueberry_list = plant_blueberry_list
        self.not_placed = True

        if random.random() < 0.5:
            self.texture_plant_blueberry = arcade.load_texture("images/water_plant1.png",
                                                               scale=SPRITE_SCALING_PLANT_BLUEBERRY)
        else:
            self.texture_plant_blueberry = arcade.load_texture("images/water_plant1.png", mirrored=True,
                                                               scale=SPRITE_SCALING_PLANT_BLUEBERRY)
        self.texture = self.texture_plant_blueberry

        # Placera ut blåbärsplantan
        self.try_place_number = 5

        self.illegal_coordinates = []
        for plant in self.plant_blueberry_list:
            coordinates = [plant.center_x - 100, plant.center_x + 100]
            self.illegal_coordinates.append(coordinates)

        while self.not_placed and self.try_place_number > 0:
            self.not_placed = False
            if random.random() < 0.5:
                test_center_x = random.randint(int(self.sw * 0.05), int(self.sw * 0.35))
            else:
                test_center_x = random.randint(int(self.sw * 0.65), int(self.sw * 0.95))
            test_center_y = random.randint(int(self.sh * self.sr), int(self.sh * self.sr * 1.3))
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
