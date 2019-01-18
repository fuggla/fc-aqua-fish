import arcade, random, math
from classes.fish import FishSprite
from fish_vars import SPRITE_SCALING_SHARK, shark_eager, shark_hungry, shark_hunt_will, shark_daydream, shark_kiss_will, shark_finforce, shark_mass, shark_size, shark_findelay, shark_hunting_spirit

# Klass för hajarna (Shark_fish)
class SharkSprite(FishSprite):
    def __init__(self, textures_shark, textures_shark_kid, food_fish_list, popcorn_list, shark_list, event=None, eager=None, hungry=None, hunt_will=None, daydream=None, finforce=None, size=None, mass=None,
                 color=None, setpos_x=None, setpos_y=None, setspeed_y=None):
        # Anropa Sprite konstruktor
        super().__init__(event)

        # Fiskarnas personlighet
        self.eager = eager or shark_eager                 # Hur ofta byter fiskarna riktning
        self.hungry = hungry or shark_hungry              # Hur intresserade är de av mat
        self.hunt_will = hunt_will or shark_hunt_will
        self.base_hungry = self.hungry
        self.daydream = daydream or shark_daydream
        self.kiss_will = shark_kiss_will

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or shark_finforce
        self.size = size or shark_size
        self.base_size = shark_size
        self.scaling = SPRITE_SCALING_SHARK
        self.mass = mass or shark_mass
        self.type = "shark"
        self.shark_list = shark_list

        self.findelay = shark_findelay          # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 8                      # Denna variabel styr hur intensivt de äter

        self.food_fish_list_b = food_fish_list
        self.food_fish_list_p = popcorn_list
        self.food_fish_list = []
        self.hunting_spirit = 0
        self.base_hunting_spirit = shark_hunting_spirit
        self.tired = 0

        # Ladda in texturer
        self.textures_grown = textures_shark
        self.textures_kid = textures_shark_kid
        if self.size < self.base_size:
            self.textures = self.textures_kid
        else:
            self.textures = self.textures_grown

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.set_texture(0)
            self.whichtexture = 11              # 11 = left1
        else:
            self.set_texture(2)
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

        self.set_food_list()

        # Kolla om de är vuxna
        if self.size < self.base_size:
            self.grown_up = False
        else:
            self.grown_up = True

        # Håll koll ifall fisken störs av någonting
        if not self.isalive or not self.relaxed == [True, True] or self.pregnant or self.partner or self.is_hooked:
            self.disturbed = True
        else:
            self.disturbed = False

        # Om de är lugna och pigga kan de vilja börja jaga mat
        if random.randrange(1000) < self.hunt_will and self.food_fish_list and self.hunting_spirit <= 0 and self.tired <= 0 and not self.disturbed and self.grown_up:
            self.hunting_spirit = random.randint(self.base_hunting_spirit / 2, self.base_hunting_spirit)

        if self.hunting_spirit <= 0 < self.tired:
            self.tired -= 1

        if self.partner or not self.food_fish_list:
            self.hunting_spirit = 0

        # Om hajarna jagar så jagar dom ordentligt
        if self.hunting_spirit > 0 and self.isalive:
            self.chase_fish()
            self.hunting_spirit -= 1
            self.tired = 500

        # Om de är lugna kan de vilja ändra riktning
        if random.randrange(1000) < self.eager and self.hunting_spirit <= 0 and not self.disturbed:
            self.random_move()

        # ifall fisken är mätt och pilsk och inte störd kan den bli sugen att pussas
        if self.health > self.base_health and random.randrange(1000) < self.kiss_will and not self.disturbed and self.grown_up:
            self.kiss_spirit = 1000

        # Om de är sugna att pussas och inte störda letar de efter en partner
        if self.kiss_spirit > 0 and not self.disturbed:
            self.find_partner(self.shark_list)

        # De tröttnas ifall de inte hittar någon
        if self.kiss_spirit > 0:
            self.kiss_spirit -= 1

        # Finns det en partner och fisken lever så flyttar den sig mot den
        if self.partner and self.isalive:
            self.move_to_partner_kiss(self.partner)

        # Om fisken är gravid så flyttar den sig mot en bra plats att lägga äggen på
        if self.pregnant and self.isalive:
            self.move_lay_egg_position()

        # Om de är lugna kan de börja dagdrömma
        if random.randrange(1000) < self.daydream and self.hunting_spirit <= 0 and not self.disturbed:
            self.acc_x = 0
            self.acc_y = 0

        if self.size < self.base_size:
            self.check_grow_up()

        if self.health <= 0:
            self.die()

        # Ta bort döda fisken som flutit upp
        if self.bottom > self.sh and self.health <= 0:
            self.kill()

        # Kolla om fisken är nära kansten och styr in den mot mitten
        # Stressa även upp den
        if self.hunting_spirit <= 0:
            self.check_edge()

        # Beräkna vattnets motstånd
        self.water_res()

        # Gör beräkningar för acceleration
        self.move_calc()

        # Gör beräkningar för hälsa
        self.health_calc()

        # Updatera animationen
        if self.hunting_spirit <= 0 and self.isalive and self.iseating == 0 and not self.is_hooked:
            if self.partner:
                self.animate_love()
            else:
                self.animate()

        # Updatera animationen ifall den jagar
        if self.hunting_spirit > 0 and self.isalive and not self.is_hooked:
            self.animate_hunt()

        # Anropa huvudklassen
        super().update()

    def set_food_list(self):
        # Skapa lista för bfish och alla popcorn
        self.food_fish_list = []
        for fish in self.food_fish_list_b:
            self.food_fish_list.append(fish)
        for popcorn in self.food_fish_list_p:
            self.food_fish_list.append(popcorn)
