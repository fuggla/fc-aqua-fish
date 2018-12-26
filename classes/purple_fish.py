
import arcade, random, math
from classes.fish import FishSprite
from vars import SPRITE_SCALING_PFISH, SCREEN_WIDTH, SCREEN_HEIGHT

# Klass för lila fiskar (Purple_fish)
class PfishSprite(FishSprite):
    def __init__(self, carrot_list):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.food_objects = carrot_list

        # texture 1 & 2 för höger och vänster
        self.texture_left1 = arcade.load_texture("images/purple_fish1.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_left2 = arcade.load_texture("images/purple_fish2.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_right1 = arcade.load_texture("images/purple_fish1.png", scale=SPRITE_SCALING_PFISH)
        self.texture_right2 = arcade.load_texture("images/purple_fish2.png", scale=SPRITE_SCALING_PFISH)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
            self.whichtexture = 11              # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21              # 21 = right1

        # Placera ut fiskarna
        self.center_x = random.randrange(self.sw * 0.8) + self.sw * 0.1
        self.center_y = random.randrange(self.sh * 0.8) + self.sh * 0.1

        # Fiskarnas personlighet
        self.eager = 5                  # Hur ofta byter fiskarna riktning
        self.hungry = 5                 # Hur intresserade är de av mat
        self.daydream = 10

        # Fiskarnas fysiska egenskaper
        self.finforce = 6
        self.size = 8
        self.mass = 8                # Default är samma som .siz<e

        self.findelay = 20              # Hur ofta viftar de med fenorna
        self.findelay_base = 20

        self.relaxed = [True, True]     # Pfish blir nervös nära kanter
        self.frame_count = 0

    def update(self):

        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * self.sw < self.center_x < 0.85 * self.sw:
            self.relaxed[0] = True
        if 0.15 * self.sh < self.center_y < 0.85 * self.sh:
            self.relaxed[1] = True

        # Om de är lugna kan de vilja ändra riktning
        if self.relaxed == [True, True] and random.randrange(1000) < self.eager:
            self.random_move()

        # Om de är lugna och kan de vilja jaga mat
        if self.relaxed == [True, True] and random.randrange(1000) < self.hungry:
            self.chase_food()

        # Om de är lugna kan de börja dagdrömma
        if self.relaxed == [True, True] and random.randrange(1000) < self.daydream:
            self.acc_x = 0
            self.acc_y = 0

        # Kolla om fisken är nära kansten och styr in den mot mitten
        # Stressa även upp den
        self.check_edge()

        # Beräkna negativ acceleration från vattnet
        self.break_x = self.size * self.change_x * math.fabs(self.change_x) / self.mass
        self.break_y = self.size * self.change_y * math.fabs(self.change_y) / self.mass

        # Hastigheten är tidigare hastighet plus positiv acceleration minus negativ acceleration
        # Här ska programmets framerate in stället för 30
        self.change_x = self.change_x + (self.acc_x - self.break_x)/30
        self.change_y = self.change_y + (self.acc_y - self.break_y)/30

        # Updatera animationen
        self.animate()

        # Stega upp intärna klocka
        self.frame_count += 1

        # Anropa huvudklassen
        super().update()


    def animate(self):
        # Animering av fiskarna

        # Ändra fenfrekvens utifrån totalacceleration
        self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y))/self.finforce + 1))

        # Vänd dem i x-hastighetens riktning
        if self.change_x < 0 and not (self.whichtexture == 11 or self.whichtexture == 12):
            self.texture = self.texture_left1
            self.whichtexture = 11
        if self.change_x > 0 and not (self.whichtexture == 21 or self.whichtexture == 22):
            self.texture = self.texture_right1
            self.whichtexture = 21
        # "self.whichtexture = 11" betyder "left texture 1"
        # "self.whichtexture = 22" betyder "right texture 2"

        # Animation riktad åt vänster
        if self.frame_count % self.findelay == 0 and self.whichtexture == 11:
            self.texture = self.texture_left2
            self.whichtexture = 12
        elif self.frame_count % self.findelay == 0 and self.whichtexture == 12:
            self.texture = self.texture_left1
            self.whichtexture = 11
        # Animation riktad åt höger
        if self.frame_count % self.findelay == 0 and self.whichtexture == 21:
            self.texture = self.texture_right2
            self.whichtexture = 22
        elif self.frame_count % self.findelay == 0 and self.whichtexture == 22:
            self.texture = self.texture_right1
            self.whichtexture = 21


