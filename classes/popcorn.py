import arcade,random,math
from vars import SPRITE_SCALING_POPCORN, SCREEN_WIDTH, SCREEN_HEIGHT, TICK_RATE, popcorn_food_value


class PopcornSprite(arcade.Sprite):
    # Klass för popcorn. Bete på kroken
    def __init__(self, hook):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        self.type = "popcorn"
        self.base_food_value = popcorn_food_value
        self.hook = hook

        img = f"assets/images/food/popcorn"
        self.texture_food1 = arcade.load_texture(f"{img}/popcorn1.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food2 = arcade.load_texture(f"{img}/popcorn2.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food3 = arcade.load_texture(f"{img}/popcorn3.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food4 = arcade.load_texture(f"{img}/popcorn4.png", scale=SPRITE_SCALING_POPCORN)
        self.texture = self.texture_food1

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
