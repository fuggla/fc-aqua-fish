import arcade,random,math
from vars import SPRITE_SCALING_BLUEBERRY, blueberry_food_value


class BlueberrySprite(arcade.Sprite):
    # Klass för blueberry
    def __init__(self, center_x, center_y):
        # Anropa Sprite konstruktor
        super().__init__()

        self.texture_food1 = arcade.load_texture("images/blueberry1.png", scale=SPRITE_SCALING_BLUEBERRY)
        self.texture_food2 = arcade.load_texture("images/blueberry2.png", scale=SPRITE_SCALING_BLUEBERRY)
        self.texture_food3 = arcade.load_texture("images/blueberry3.png", scale=SPRITE_SCALING_BLUEBERRY)
        self.texture_food4 = arcade.load_texture("images/blueberry4.png", scale=SPRITE_SCALING_BLUEBERRY)
        self.texture = self.texture_food1

        # Placera ut moroten
        self.center_x = center_x
        self.center_y = center_y

        self.food_value = blueberry_food_value     # Hur mycket mat finns på bäret

    def update(self):
        pass
        super().update()

    def eaten(self):
        self.food_value -= 1
        if self.food_value == 0:
            self.kill()