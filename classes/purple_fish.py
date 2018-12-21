
import arcade,random

# Klass för lila fiskar (Purple_fish)
class PfishSprite(arcade.Sprite):
    def __init__(self,SPRITE_SCALING_PFISH,SCREEN_WIDTH,SCREEN_HEIGHT):
        # Anropa Sprite konstruktor
        super().__init__()

        global sw
        global sh
        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        # texture för höger och vänster
        self.texture_left1 = arcade.load_texture("images/purple_fish1.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_left2 = arcade.load_texture("images/purple_fish2.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_right1 = arcade.load_texture("images/purple_fish1.png", scale=SPRITE_SCALING_PFISH)
        self.texture_right2 = arcade.load_texture("images/purple_fish2.png", scale=SPRITE_SCALING_PFISH)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
        else:
            self.texture = self.texture_right1
        self.ani_left = 0       # variabler som styr animeringen
        self.ani_left_add = 0
        self.ani_right = 0
        self.ani_right_add = 0

        # Placera ut fiskarna
        self.center_x = random.randrange(sw * 0.8) + sw * 0.1
        self.center_y = random.randrange(sh * 0.8) + sh * 0.1
        # Starthastihet
        self.change_x = 0  # x_hastighet
        self.change_y = 0  # y_hastighet
        self.eager = 5 + random.randrange(5)
        self.relaxed = [True, True]                     # Pfish blir nervös nära kanter

    def update(self):
        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.10 * sw < self.center_x < 0.90 * sw:
            self.relaxed[0] = True
        if 0.10 * sh < self.center_y < 0.90 * sh:
            self.relaxed[1] = True

        if self.relaxed == [True, True]:
            # Om de är lugna så rör de sig normalt
            if random.randrange(100) < self.eager:
                self.change_x = random.random() * 2 - 1
                self.change_y = random.random() * 2 - 1
            # Slumpfaktor som gör att de stannar upp och funderar
        if random.randrange(100) == 0:
            self.change_x = 0
            self.change_y = 0

        # Alla dessa if kollar kanter, styr in dem mot mitten och stressar upp dem
        if self.center_x > sw * 0.95:
            self.change_x = -2
            self.relaxed[0] = False
        if self.center_x < sw * 0.05:
            self.change_x = 2
            self.relaxed[0] = False

        if self.center_y > sh * 0.95:
            self.change_y = -2
            self.relaxed[1] = False
        if self.center_y < sh * 0.05:
            self.change_y = 2
            self.relaxed[1] = False

        # Vänd dem i x-hastighetens riktning
        if self.change_x < 0:
            if self.ani_left <= 0:
                self.texture = self.texture_left1
                self.ani_left_add = 1
            if self.ani_left >= 10:
                self.texture = self.texture_left2
                self.ani_left_add = -1
            self.ani_right = 0

        if self.change_x > 0:
            if self.ani_right <= 0:
                self.texture = self.texture_right1
                self.ani_right_add = 1
            if self.ani_right >= 10:
                self.texture = self.texture_right2
                self.ani_right_add = -1
            self.ani_left = 0

        if self.change_x == 0:
            self.ani_left = 0
            self.ani_right = 0

        self.ani_left = self.ani_left + self.ani_left_add
        self.ani_right = self.ani_right + self.ani_right_add

        # Anropa huvudklassen
        super().update()
