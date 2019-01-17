import arcade,random,math
from vars import SPRITE_SCALING_POPCORN, SCREEN_WIDTH, SCREEN_HEIGHT, TICK_RATE, popcorn_food_value


class PopcornSprite(arcade.Sprite):
    # Klass för popcorn. Bete på kroken
    def __init__(self, textures_popcorn, hook):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        self.type = "popcorn"
        self.base_food_value = popcorn_food_value
        self.hook = hook

        self.textures = textures_popcorn
        self.set_texture(0)

        self.angle = 40
        self.x_diff = 20
        self.y_diff = - 30
        self.center_x = self.hook.center_x + self.x_diff
        self.center_y = self.hook.center_y + self.y_diff

        # Definiera variabler
        self.food_value = popcorn_food_value     # Hur mycket mat finns på popcornet

    def update(self):

        self.center_x = self.hook.center_x + self.x_diff
        self.center_y = self.hook.center_y + self.y_diff

        # Anropa huvudklassen
        super().update()

    def get_name(self):
        return "popcorn"
