import arcade,random,math

# Klass för lila fiskar (Purple_fish)
class Carrot(arcade.Sprite):
    def __init__(self, SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Anropa Sprite konstruktor
        super().__init__()

        global sw
        global sh
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        self.texture_carrot1 = arcade.load_texture("images/carrot1.png", scale=SPRITE_SCALING_CARROT)
