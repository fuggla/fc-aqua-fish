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
            coordinates = range(plant.center_x - 50, plant.center_x + 50)
            self.illegal_coordinates.append(coordinates)

        while self.not_placed and self.try_place_number > 0:
            self.not_placed = False
            self.center_x = random.randint(int(self.sw * 0.05), int(self.sw * 0.95))
            self.center_y = random.randint(int(self.sh * self.sr), int(self.sh * self.sr * 1.3))
            for coordinates in self.illegal_coordinates:
                for x_cor in coordinates:
                    if self.center_x == x_cor:
                        self.not_placed = True


    def update(self):
        pass
        # Anropa huvudklassen
        super().update()
