
import arcade,random

# Klass för lila fiskar (Purple_fish)
class PfishSprite(arcade.Sprite):
    def __init__(self,SPRITE_SCALING_PFISH,SCREEN_WIDTH,SCREEN_HEIGHT):
        # Anropa Sprite konstruktor
        super().__init__()

        # texture för höger och vänster
        self.texture_left1 = arcade.load_texture("images/purple_fish1.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_left2 = arcade.load_texture("images/purple_fish2.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_right1 = arcade.load_texture("images/purple_fish1.png", scale=SPRITE_SCALING_PFISH)
        self.texture_right2 = arcade.load_texture("images/purple_fish2.png", scale=SPRITE_SCALING_PFISH)
        # Default = right
        self.texture = self.texture_right1
        self.ani_left = 0       # variabler som styr animeringen
        self.ani_left_add = 0
        self.ani_right = 0
        self.ani_right_add = 0

        # Placera ut fiskarna
        self.center_x = random.randrange(SCREEN_WIDTH * 0.8) + SCREEN_WIDTH * 0.1
        self.center_y = random.randrange(SCREEN_HEIGHT * 0.8) + SCREEN_HEIGHT * 0.1
        # Starthastihet
        self.change_x = 0  # x_hastighet
        self.change_y = 0  # y_hastighet
        self.pathcounter = random.random() * 200        # Variable som styr hur länge de gör saker
        self.relaxed = [True, True]                     # Pfish blir nervös nära kanter
