import arcade, random, math
from vars import SPRITE_SCALING_PLANT_BLUEBERRY, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO


class PlantBlueberry(arcade.Sprite):
    # Klass för blåbärsplantan
    def __init__(self):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        if random.random() < 0.5:
            self.texture_plant_blueberry = arcade.load_texture("images/water_plant1.png",
                                                               scale=SPRITE_SCALING_PLANT_BLUEBERRY)
        else:
            self.texture_plant_blueberry = arcade.load_texture("images/water_plant1.png", mirrored=True,
                                                               scale=SPRITE_SCALING_PLANT_BLUEBERRY)
        self.texture = self.texture_plant_blueberry

        # Placera ut blåbärsplantan
        self.center_x = random.randint(int(self.sw * 0.1), int(self.sw * 0.9))
        self.center_y = random.randint(int(self.sh * self.sr / 2), int(self.sh * self.sr))

    def update(self):
        pass
        # Anropa huvudklassen
        super().update()
