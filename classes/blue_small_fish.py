
import arcade, random, math
from classes.fish import FishSprite
from vars import SCREEN_WIDTH, SCREEN_HEIGHT
from fish_vars import SPRITE_SCALING_BFISH, bfish_eager, bfish_hungry, bfish_conformity, bfish_daydream, bfish_finforce, bfish_mass, bfish_size, bfish_findelay

# Klass för små blå fiskar (blue_fish)
class BfishSprite(FishSprite):
    def __init__(self, carrot_list, bfish_list, eager=None, hungry=None, conformity=None, daydream=None, finforce=None, size=None, mass=None, color=None):
        # Anropa Sprite konstruktor
        super().__init__()

        # Fiskarnas personlighet
        self.eager = eager or bfish_eager           # Hur ofta byter fiskarna riktning
        self.hungry = hungry or bfish_hungry        # Hur intresserade är de av mat
        self.base_hungry = self.hungry
        self.conformity = conformity or bfish_conformity
        self.daydream = daydream or bfish_daydream

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or bfish_finforce
        self.size = size or bfish_size
        self.mass = mass or bfish_mass
        self.color = color or "blue"
        self.type = "bfish"

        self.findelay = bfish_findelay  # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 5

        self.relaxed = [True, True]  # Pfish blir nervös nära kanter
        self.frame_count = 0

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.food_objects = carrot_list
        self.shoal_objects = bfish_list

        # texture 1 & 2 för höger och vänster
        scale_factor = SPRITE_SCALING_BFISH * self.size / 8
        if color == "green":
            self.texture_left1 = arcade.load_texture("images/green_fish1.png", mirrored=True, scale=scale_factor)
            self.texture_left2 = arcade.load_texture("images/green_fish2.png", mirrored=True, scale=scale_factor)
            self.texture_left8 = arcade.load_texture("images/blue_small_fish_eat.png", mirrored=True, scale=scale_factor)
            self.texture_right1 = arcade.load_texture("images/green_fish1.png", scale=scale_factor)
            self.texture_right2 = arcade.load_texture("images/green_fish2.png", scale=scale_factor)
            self.texture_right8 = arcade.load_texture("images/blue_small_fish_eat.png", scale=scale_factor)
        else:
            self.texture_left1 = arcade.load_texture("images/blue_small_fish1.png", mirrored=True, scale=scale_factor)
            self.texture_left2 = arcade.load_texture("images/blue_small_fish2.png", mirrored=True, scale=scale_factor)
            self.texture_left8 = arcade.load_texture("images/blue_small_fish_eat.png", mirrored=True, scale=scale_factor)
            self.texture_right1 = arcade.load_texture("images/blue_small_fish1.png", scale=scale_factor)
            self.texture_right2 = arcade.load_texture("images/blue_small_fish2.png", scale=scale_factor)
            self.texture_right8 = arcade.load_texture("images/blue_small_fish_eat.png", scale=scale_factor)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
            self.whichtexture = 11  # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21  # 21 = right1

        # Placera ut fiskarna
        self.center_x = random.randrange(int(self.sw * 0.7)) + int(self.sw * 0.1)
        self.center_y = random.randrange(int(self.sh * 0.7)) + int(self.sh * 0.1)

    def update(self):

        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * self.sw < self.center_x < 0.85 * self.sw:
            self.relaxed[0] = True
        if 0.15 * self.sh < self.center_y < 0.85 * self.sh:
            self.relaxed[1] = True

        # Om de är lugna kan de vilja ändra riktning
        if self.relaxed == [True, True] and random.randrange(1000) < self.eager and self.isalive:
            self.random_move()

        if self.relaxed == [True, True] and random.randrange(1000) < self.conformity and self.isalive:
            self.shoal_move()

        if self.relaxed == [True, True] and random.randrange(1000) < self.hungry and self.isalive:
            self.chase_food()

        # Om de är lugna kan de börja dagdrömma
        if self.relaxed == [True, True] and random.randrange(1000) < self.daydream and self.isalive:
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
        if self.isalive:
            self.animate()

        # Anropa huvudklassen
        super().update()
    def shoal_move(self):
        """ Hämta in koordinater och hastihet från närmsta två blue_small_fish """
        if len(self.shoal_objects) > 1:

            dist1 = 1000000000      # variable där avstånet (i kvadrat) till närmaste bfish sparas
            dist2 = 1000000000

            fish1 = 0               # index för närmaste bfish
            fish2 = 0               # index för näst närmaste bfish

            index = 0

            # Stega igenom alla fiskar och spara index och avstånd om de är närmast eller näst närmast
            for fish in self.shoal_objects:
                if fish.center_x == self.center_x and fish.center_y == self.center_y:   # Räkna bort sig själv
                    pass
                elif ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2) < dist1:
                    dist1 = ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2)
                    fish1 = index
                elif ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2) < dist2:
                    dist2 = ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2)
                    fish2 = index
                index += 1
            if len(self.shoal_objects) == 2:
                # Spara x- & y-positioner för närmaste och näst närmaste fisk
                midpos_x = self.shoal_objects[fish1].center_x
                midpos_y = self.shoal_objects[fish1].center_y


            elif len(self.shoal_objects) >= 3:
                # Spara x- & y-positioner för närmaste och näst närmaste fisk
                pos1_x = self.shoal_objects[fish1].center_x
                pos1_y = self.shoal_objects[fish1].center_y

                pos2_x = self.shoal_objects[fish2].center_x
                pos2_y = self.shoal_objects[fish2].center_y

                # Beräkna medelvärde för dessa positioner
                midpos_x = (pos1_x + pos2_x) / 2
                midpos_y = (pos1_y + pos2_y) / 2

            # Beräkna vinkel mot medelvärdet av positionerna och accelerera ditåt
            ang = math.atan2((midpos_y - self.center_y), (midpos_x - self.center_x))
            shoal_speed = random.random() * self.finforce / self.mass
            self.acc_x = shoal_speed * math.cos(ang)
            self.acc_y = shoal_speed * math.sin(ang)