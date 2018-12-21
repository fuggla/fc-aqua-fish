
import arcade,random,math
from classes.carrot import CarrotSprite

# Klass för lila fiskar (Purple_fish)
class PfishSprite(arcade.Sprite):
    def __init__(self, SPRITE_SCALING_PFISH, SCREEN_WIDTH, SCREEN_HEIGHT):
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
            self.whichtexture = 11              # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21              # 21 = right1

        self.frame_count = 0


        # Placera ut fiskarna
        self.center_x = random.randrange(sw * 0.8) + sw * 0.1
        self.center_y = random.randrange(sh * 0.8) + sh * 0.1

        # Starthastihet
        self.change_x = 0       # x_hastighet
        self.change_y = 0       # y_hastighet
        self.acc_x = 0          # x_acceleration
        self.acc_y = 0          # y_acceleration

        # Fiskarnas personlighet
        self.eager = 5
        self.daydream = 10
        self.findelay = 20              # Hur ofta viftar de med fenorna
        self.findelay_base = 20

        self.waterres = 0.99            # Bromsande kraft på fisken från vattnet
        self.maxspeed = 2               # Fiskens maxxhastighet (gäller då fisken är lugn)
        self.relaxed = [True, True]     # Pfish blir nervös nära kanter

    def update(self):
        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * sw < self.center_x < 0.85 * sw:
            self.relaxed[0] = True
        if 0.15 * sh < self.center_y < 0.85 * sh:
            self.relaxed[1] = True

        # Om de är lugna kan de vilja ändra riktning
        if self.relaxed == [True, True] and random.randrange(1000) < self.eager:
            self.acc_x = random.random() * 0.1 - 0.05
            self.acc_y = random.random() * 0.1 - 0.05

        # Om de är lugna kan de börja dagdrömma
        if self.relaxed == [True, True] and random.randrange(1000) < self.daydream:
            self.acc_x = 0
            self.acc_y = 0

        # Alla dessa if kollar kanter, styr in dem mot mitten och stressar upp dem
        if self.center_x > sw * 0.90:
            self.acc_x = -0.1
            self.relaxed[0] = False
        if self.center_x < sw * 0.10:
            self.acc_x = 0.1
            self.relaxed[0] = False

        if self.center_y > sh * 0.90:
            self.acc_y = -0.1
            self.relaxed[1] = False
        if self.center_y < sh * 0.10:
            self.acc_y = 0.1
            self.relaxed[1] = False

        # Accelerera ifall maxhastigheten inte är nådd
        if math.sqrt(self.change_x**2 + self.change_y**2) <= self.maxspeed:
            self.change_x = self.change_x + self.acc_x
            self.change_y = self.change_y + self.acc_y

        # Accelerationen minskar ifall den är avslappnad
        if self.relaxed == [True, True]:
            self.acc_x = self.acc_x * self.waterres
            self.acc_y = self.acc_y * self.waterres

        # Bromsa upp vattnet
        self.change_x = self.change_x * self.waterres
        self.change_y = self.change_y * self.waterres

        # Updatera animationen
        self.animate()

        # Anropa huvudklassen
        super().update()

        print(CarrotSprite.get_coordinates(self))

    def animate(self):
        # Animering av fiskarna

        # Ändra fenfrekvens utifrån totalhastighet
        self.findelay = int(self.findelay_base/(math.sqrt(self.change_x**2+self.change_y**2)+1))

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

        # Stega upp fiskarnas intärna klocka
        self.frame_count += 1
