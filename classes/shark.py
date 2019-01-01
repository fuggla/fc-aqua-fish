import arcade, random, math
from classes.fish import FishSprite
from vars import SCREEN_WIDTH, SCREEN_HEIGHT
from fish_vars import SPRITE_SCALING_PFISH, pfish_eager, pfish_hungry, pfish_daydream, pfish_finforce, pfish_mass, pfish_size, pfish_findelay

# Klass för hajarna (Shark_fish)
class SharkSprite(FishSprite):
    def __init__(self, food_fish_list, eager=None, hungry=None, daydream=None, finforce=None, size=None, mass=None,
                 color=None, setpos_x=None, setpos_y=None, setspeed_y=None):
        # Anropa Sprite konstruktor
        super().__init__()

        # Fiskarnas personlighet
        self.eager = eager or shark_eager                 # Hur ofta byter fiskarna riktning
        self.hungry = hungry or shark_hungry              # Hur intresserade är de av mat
        self.base_hungry = self.hungry
        self.daydream = daydream or shark_daydream

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or shark_finforce
        self.size = size or shark_size
        self.mass = mass or shark_mass
        self.type = "shark"

        self.findelay = pfish_findelay          # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 8                      # Denna variabel styr hur intensivt de äter

        self.relaxed = [True, True]             # Pfish blir nervös nära kanter
        self.frame_count = 0

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.food_fish_list = food_fish_list

        # texture 1 & 2 för höger och vänster
        scale_factor = SPRITE_SCALING_PFISH*self.size/8
        self.texture_left1 = arcade.load_texture("images/shark1.png", mirrored=True, scale=scale_factor)
        self.texture_left2 = arcade.load_texture("images/shark2.png", mirrored=True, scale=scale_factor)
        self.texture_left_eat1 = arcade.load_texture("images/shark_eat1.png", mirrored=True, scale=scale_factor)
        self.texture_left_eat2 = arcade.load_texture("images/shark_eat2.png", mirrored=True, scale=scale_factor)
        self.texture_right1 = arcade.load_texture("images/shark1.png", scale=scale_factor)
        self.texture_right2 = arcade.load_texture("images/shark2.png", scale=scale_factor)
        self.texture_right_eat1 = arcade.load_texture("images/shark_eat1.png", scale=scale_factor)
        self.texture_right_eat2 = arcade.load_texture("images/shark_eat2.png", scale=scale_factor)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
            self.whichtexture = 11              # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21              # 21 = right1

        # Placera ut fiskarna
        self.center_x = setpos_x or random.randrange(int(self.sw * 0.8)) + int(self.sw * 0.1)
        self.center_y = setpos_y or random.randrange(int(self.sh * 0.8)) + int(self.sh * 0.1)
        self.change_y = setspeed_y or 0
