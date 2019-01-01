import arcade, random, math
from classes.fish import FishSprite
from vars import SCREEN_WIDTH, SCREEN_HEIGHT
from fish_vars import SPRITE_SCALING_SHARK, shark_eager, shark_hungry, shark_daydream, shark_finforce, shark_mass, shark_size, shark_findelay, shark_hunting_spirit

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

        self.findelay = shark_findelay          # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 8                      # Denna variabel styr hur intensivt de äter

        self.food_fish_list = food_fish_list
        self.hunting_spirit = 0
        self.base_hunting_spirit = shark_hunting_spirit


        self.relaxed = [True, True]             # Pfish blir nervös nära kanter
        self.frame_count = 0

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        # texture 1 & 2 för höger och vänster
        scale_factor = SPRITE_SCALING_SHARK*self.size/8
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

    def update(self):

        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * self.sw < self.center_x < 0.85 * self.sw:
            self.relaxed[0] = True
        if 0.15 * self.sh < self.center_y < 0.85 * self.sh:
            self.relaxed[1] = True

        # Om de är lugna och kan de vilja börja jaga mat
        if self.relaxed == [True, True] and random.randrange(1000) < self.hungry and self.isalive:
            self.hunting_spirit = random.randint(self.base_hunting_spirit / 2, self.base_hunting_spirit)

        # Om hajarna jagar så jagar dom ordentligt
        if self.hunting_spirit > 0:
            self.chase_fish()
            self.hunting_spirit -= 1

        # Om de är lugna kan de vilja ändra riktning
        if self.relaxed == [True, True] and random.randrange(1000) < self.eager and self.isalive and self.hunting_spirit <= 0:
            self.random_move()

        # Om de är lugna kan de börja dagdrömma
        if self.relaxed == [True, True] and random.randrange(1000) < self.daydream and self.isalive and self.hunting_spirit <= 0:
            self.acc_x = 0
            self.acc_y = 0

        if self.health <= 0:
            self.die()

        # Kolla om fisken är nära kansten och styr in den mot mitten
        # Stressa även upp den
        self.check_edge()

        # Beräkna vattnets motstånd
        self.water_res()

        # Gör beräkningar för acceleration
        self.move_calc()

        # Gör beräkningar för hälsa
        self.health_calc()

        # Updatera animationen
        if self.hunting_spirit <= 0 and self.isalive:
            self.animate()

        # Updatera animationen ifall den jagar
        if self.hunting_spirit > 0 and self.isalive:
            self.animate_hunt()

        # Anropa huvudklassen
        super().update()