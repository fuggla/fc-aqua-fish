import arcade,random,math
from vars import SPRITE_SCALING_BLUEBERRY, blueberry_food_value


class BlueberrySprite(arcade.Sprite):
    # Klass för blueberry
    def __init__(self, center_x, center_y):
        # Anropa Sprite konstruktor
        super().__init__()

        self.texture_blueberry1 = arcade.load_texture("images/blueberry1.png", scale=SPRITE_SCALING_CARROT)
        self.texture_blueberry2 = arcade.load_texture("images/blueberry2.png", scale=SPRITE_SCALING_CARROT)
        self.texture_blueberry3 = arcade.load_texture("images/blueberry3.png", scale=SPRITE_SCALING_CARROT)
        self.texture_blueberry4 = arcade.load_texture("images/blueberry4.png", scale=SPRITE_SCALING_CARROT)
        self.texture = self.texture_blueberry1

        # Placera ut moroten
        self.center_x = center_y
        self.center_y = center_x

        self.food_value = blueberry_food_value     # Hur mycket mat finns på bäret

    def update(self):
        pass
        super().update()

    def eaten(self):
        self.food_value -= 1
        if self.food_value == 0:
            self.kill()