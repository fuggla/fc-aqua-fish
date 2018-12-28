import arcade, random, math
from classes.fish import FishSprite
from vars import SPRITE_SCALING_BFISH, SCREEN_WIDTH, SCREEN_HEIGHT, bfish_eager, bfish_hungry, bfish_daydream, bfish_finforce, bfish_mass, bfish_size, bfish_findelay

# Klass för små blå fiskar (blue_fish)
class BfishSprite(FishSprite):
    def __init__(self, carrot_list, eager=None, hungry=None, daydream=None, finforce=None, size=None, mass=None, color=None):
        # Anropa Sprite konstruktor
        super().__init__()

        # Fiskarnas personlighet
        self.eager = eager or bfish_eager           # Hur ofta byter fiskarna riktning
        self.hungry = hungry or bfish_hungry        # Hur intresserade är de av mat
        self.daydream = daydream or bfish_daydream

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or bfish_finforce
        self.size = size or bfish_size
        self.mass = mass or bfish_mass
        self.color = color or "blue"

        self.findelay = bfish_findelay  # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay

        self.relaxed = [True, True]  # Pfish blir nervös nära kanter
        self.frame_count = 0

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.food_objects = carrot_list

        # texture 1 & 2 för höger och vänster
        scale_factor = SPRITE_SCALING_BFISH * self.size / 8
        if color == "green":
            self.texture_left1 = arcade.load_texture("images/green_fish1.png", mirrored=True, scale=scale_factor)
            self.texture_left2 = arcade.load_texture("images/green_fish2.png", mirrored=True, scale=scale_factor)
            self.texture_right1 = arcade.load_texture("images/green_fish1.png", scale=scale_factor)
            self.texture_right2 = arcade.load_texture("images/green_fish2.png", scale=scale_factor)
        else:
            self.texture_left1 = arcade.load_texture("images/blue_fish1.png", mirrored=True, scale=scale_factor)
            self.texture_left2 = arcade.load_texture("images/blue_fish2.png", mirrored=True, scale=scale_factor)
            self.texture_right1 = arcade.load_texture("images/blue_fish1.png", scale=scale_factor)
            self.texture_right2 = arcade.load_texture("images/blue_fish2.png", scale=scale_factor)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
            self.whichtexture = 11  # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21  # 21 = right1

        # Placera ut fiskarna
        self.center_x = random.randrange(self.sw * 0.8) + self.sw * 0.1
        self.center_y = random.randrange(self.sh * 0.8) + self.sh * 0.1