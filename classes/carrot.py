import arcade,random,math

# Klass för lila fiskar (Purple_fish)
class CarrotSprite(arcade.Sprite):
    def __init__(self, SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Anropa Sprite konstruktor
        super().__init__()

        global sw
        global sh
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        self.texture_carrot1 = arcade.load_texture("images/carrot1.png", scale=SPRITE_SCALING_CARROT)

        self.texture = self.texture_carrot1

        # Placera ut moroten
        self.center_x = random.randrange(sw * 0.8) + sw * 0.1
        self.center_y = random.randrange(sh * 0.8) + sh * 0.1

    def update(self):

        # Anropa huvudklassen
        super().update()