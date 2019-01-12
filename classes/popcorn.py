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

        img = f"assets/images/food/popcorn"
        self.texture_food1 = arcade.load_texture(f"{img}/popcorn1.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food2 = arcade.load_texture(f"{img}/popcorn2.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food3 = arcade.load_texture(f"{img}/popcorn3.png", scale=SPRITE_SCALING_POPCORN)
        self.texture_food4 = arcade.load_texture(f"{img}/popcorn4.png", scale=SPRITE_SCALING_POPCORN)
        self.texture = self.texture_food1

        self.center_x = hook.center_x + 100
        self.center_y = hook.center_y - 100

        # Definiera variabler
        self.food_value = popcorn_food_value     # Hur mycket mat finns på popcornet

    def update(self):
        pass

        # Anropa huvudklassen
        super().update()
