
import arcade, random, math, csv
from vars import TICK_RATE, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO
from classes.fish_animate import FishAnimate
from classes.fish_move import FishMove

# Läs fisknamn från names.csv
fish_names = []
with open('assets/names.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        fish_names.append([row[1], row[0]])
fish_names_length = len(fish_names)

"""
Överklass för fish. Alla gemensamma variabler och alla metoder finns här och i fish_aminate + fish_move
"""


class FishSprite(arcade.Sprite, FishAnimate, FishMove):
    def __init__(self, event=None):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.sr = SAND_RATIO

        # Definiera hastighet och acceleration
        self.change_x = 0       # x_hastighet
        self.change_y = 0       # y_hastighet
        self.acc_x = 0          # positiv x_acceleration
        self.acc_y = 0          # negativ y_acceleration
        self.break_x = 0        # negativ x_acceleration
        self.break_y = 0        # negativ y_acceleration

        # Definiera fiskegenskaper
        self.health = random.randint(10000, 15000)      # Detta är fiskarnas liv. Sjunker konstant men ökar av mat
        self.base_health = self.health
        self.hunting_spirit = 0                         # Denna variabel styr hur länge hajarna orkar jaga
        self.isalive = True
        self.is_hooked = False
        self.disturbed = False                          # Denna variable är True när fiskarnas beteendemönster bryts
        self.relaxed = [True, True]                     # Fiskarna blir nervösa nära kanterna
        self.hook = None
        self.hook_bite_pos_diff = [20, -30]             # Variable för positionen på kroken fisken fastnar
        self.eat_speed = 10                             # Animationshastighet då de äter
        self.iseating = 0                               # Variable för att stanna upp lite kort efter de ätit
        self.tick_rate = TICK_RATE                      # Tickrate för simuleringen (def=60 fps)
        self.is_hunting = False

        # Variabler för statistik
        self.frame_count = 0                            # Denna variabel innehåller fiskarnas livstid i "ticks"
        self.eaten_fish = 0                             # Antal uppätna fiskar
        self.eaten_carrots = 0                          # Antal ätna (=tagit sista tuggan på) morötter
        self.eaten_blueberries = 0                      # Antal ätna (=tagit sista tuggan på) blåbär
        self.laid_eggs = 0                              # Antal lagda ägg
        self.kiss_amount = 0                            # Antal gånger fisken har pussats

        # För kommunikation ut från objekt
        self.event = event or None

        # För förflyttning med muspekare
        self.dragged = False
        self.drag_speed = [0, 0]

        # Dessa variabler styr reproduktionen av fiskarna
        self.name_gender = fish_names[random.randrange(fish_names_length)]
        self.partner = None
        self.pregnant = False
        self.ready_to_lay_egg = False
        self.kiss_spirit = 0
        self.egg_postition = [0, 0]
        self.grown_up = True

        # Här ställs fiskaras sexualitet in
        rand = random.random()
        # För damfisk
        if self.name_gender[1] == "f":
            if rand < 0.95:
                self.attraction = "m"
            elif 0.98 >= rand >= 0.95:
                self.attraction = "f"
            else:
                self.attraction = "open minded"
        # För herrfisk
        if self.name_gender[1] == "m":
            if rand < 0.95:
                self.attraction = "f"
            elif 0.98 >= rand >= 0.95:
                self.attraction = "m"
            else:
                self.attraction = "open minded"
        # För fiskar som definierar sig som genderfluid
        if self.name_gender[1] == "g":
            if rand < 0.2:
                self.attraction = "f"
            elif 0.2 >= rand >= 0.4:
                self.attraction = "m"
            else:
                self.attraction = "open minded"

    def check_edge(self):
        # Kolla om fisken är nära kanten, styr in dem mot mitten och stressa upp den
        if self.isalive:
            if self.center_x > self.sw * 0.94:
                self.acc_x = - self.finforce / self.mass
                self.relaxed[0] = False
            if self.center_x < self.sw * 0.06:
                self.acc_x = self.finforce / self.mass
                self.relaxed[0] = False

            if self.center_y > self.sh * 0.94:
                self.acc_y = - self.finforce / self.mass
                self.relaxed[1] = False
            if self.center_y < self.sh * 0.06:
                self.acc_y = self.finforce / self.mass
                self.relaxed[1] = False

    def check_grow_up(self):
        if self.frame_count >= 2000:
            self.size = self.base_size
            self.textures = self.textures_grown

    def die(self):
        self.isalive = False
        self.acc_x = 0
        self.acc_y = .1
        if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
            self.angle = 180
            self.set_texture(2)
        if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
            self.angle = 180
            self.set_texture(0)

    def drag_sprite(self, x, y, dx, dy):
        self.center_x = x
        self.center_y = y
        self.drag_speed = [dx, dy]

    def eat_fish(self, prey):
        if self.hunting_spirit > 0:
            self.health += 10000
            self.iseating = 10          # Denna variabel håller kvar hajen en stund då den bitit

            self.hunting_spirit = 0
            self.angle = math.degrees(math.atan2(prey.center_y - self.center_y, prey.center_x - self.center_x))
            if -90 < self.angle < 90:
                self.set_texture(2)
            else:
                self.angle += 180
                self.set_texture(0)

            prey.kill()
            self.eaten_fish += 1
            self.event.put(self.get_name() + " ate " + prey.get_name())
            arcade.play_sound("assets/sound_effects/eat.wav")  # Spela ätljud

    def eat_food(self, food, chew):
        # Sätt vatiabel så att fiskarna vet att de äter
        if self.iseating <= 10:
            self.iseating += 1
        self.health += 75

        # Beräkna vinkel mot moroten fisken äter
        ang_rad = math.atan2((food.center_y - self.center_y), (food.center_x - self.center_x))
        ang_deg = math.degrees(ang_rad)     # omvandla till degrees
        self.angle = ang_deg
        self.animate_eat_food()

        food.food_value -= chew                     # Fiskarna äter moroten
        if food.food_value <= food.base_food_value * 0.75:
            food.set_texture(1)
        if food.food_value <= food.base_food_value * 0.50:
            food.set_texture(2)
        if food.food_value <= food.base_food_value * 0.25:
            food.set_texture(3)
        if food.food_value <= 0:                    # När moroten är slut försvinner den
            if food.type == "blueberry":            # Samla statistik
                self.eaten_blueberries += 1
            else:
                self.eaten_carrots += 1
            food.kill()                             # Maten har nu hamnat i fiskmagen

    def find_partner(self, possible_partner_list):
        # metod för att hitta en villig partner
        # Spara alla möjliga partners koordinater i patner_list
        # Loopen letar efter villiga partners med kön som fisken attraheras av
        if possible_partner_list:
            attraction_list = []
            for partner in possible_partner_list:
                if self == partner:
                    pass
                elif self.attraction == "m" and partner.name_gender[1] == "m" and partner.kiss_spirit > 0 and partner.iseating == 0 and not partner.partner:
                    attraction_list.append(partner)
                elif self.attraction == "f" and partner.name_gender[1] == "f" and partner.kiss_spirit > 0 and partner.iseating == 0 and not partner.partner:
                    attraction_list.append(partner)
                elif self.attraction == "open minded" and partner.kiss_spirit > 0 and partner.iseating == 0 and not partner.partner:
                    attraction_list.append(partner)

            if attraction_list:
                # Kolla vilka möjliga partners fisken attraheras av som attraheras av fisken
                partner_list = []
                for partner in attraction_list:
                    if partner.attraction == "m" and self.name_gender[1] == "m":
                        partner_list.append(partner)
                    elif partner.attraction == "f" and self.name_gender[1] == "f":
                        partner_list.append(partner)
                    elif partner.attraction == "open minded":
                        partner_list.append(partner)

                # I slutändan är det omöjligt att veta vad som får två fiskar att bli kära i varandra
                if partner_list:
                    partner = random.choice(partner_list)

                    # Spara kärleken i variabeln "partner"
                    self.partner = partner
                    partner.partner = self
                    self.iseating = 0
                    partner.iseating = 0

    def get_lay_egg_position(self):
        # Metod för att hitta en plats där fisken kan lägga ägg
        self.egg_postition[0] = random.randrange(int(self.sw * 0.1), int(self.sw * 0.9))
        self.egg_postition[1] = random.randrange(int(self.sh * self.sr * 0.3), int(self.sh * self.sr))

    def get_name(self):
        return self.name_gender[0]

    def health_calc(self):
        # Fiskarna blir hungrigare då de har låg hälsa
        if self.health < self.base_health * 0.75:
            self.hungry = self.base_hungry * 2

        if self.health < self.base_health * 0.60:
            self.hungry = self.base_hungry * 5

        if self.health < self.base_health * 0.50:
            self.hungry = self.base_hungry * 10

        if self.health < self.base_health * 0.25:
            self.hungry = self.base_hungry * 100

        # Stega upp intärna klocka
        self.frame_count += 1

        # Stega ner livsmätaren
        self.health -= 1

        if self.is_hooked and self.bottom > self.sh:
            self.kill()

    def hooked(self, hook):
        self.is_hooked = True
        self.hook = hook

    def is_mouse_on(self, pointer):
        if arcade.check_for_collision(self, pointer):
            return True

    def print_stats(self, left, right):
        health = math.ceil(self.health / self.base_health * 100)
        if self.is_hunting:
            status = "Hunting"
        elif self.pregnant:
            status = "Pregnant"
        elif (health > 100):
            status = "Aroused"
        elif (health > 85):
            status = "Satisfied"
        elif (health > 50):
            status = "Hungry"
        else:
            status = "Starving"

        if self.name_gender[1] == "f":
            gender = "female"
        elif self.name_gender[1] == "m":
            gender = "male"
        else:
            gender = "gender fluid"

        if self.attraction == "f":
            attraction = "female"
        elif self.attraction == "m":
            attraction = "male"
        else:
            attraction = "open_minded"

        if self.type == "shark":
            rows = [
                [self.name_gender[0], gender],
                ["Attraction", attraction],
                ["Status", status],
                ["Age", math.ceil(self.frame_count / 60)],
                ["Health", str(health) + "%"],
                ["Fish eaten", self.eaten_fish],
                ["Total kisses", self.kiss_amount],
                ["Eggs laid", self.laid_eggs]]
        else:
            rows = [
                [self.name_gender[0], gender],
                ["Attraction", attraction],
                ["Status", status],
                ["Age", math.ceil(self.frame_count / 60)],
                ["Health", str(health) + "%"],
                ["Food eaten", self.eaten_carrots + self.eaten_blueberries],
                ["Total kisses", self.kiss_amount],
                ["Eggs laid", self.laid_eggs]]
        for column in rows:
            left(column[0])
            right(column[1])

    def release(self):
        # Metod som ger fiskarna hastighet då de släpps av muspekaren
        self.change_x = self.drag_speed[0]  # Ställ in spritens x-hastighet
        self.change_y = self.drag_speed[1]  # Ställ in spritens y-hastighet

    def water_res(self):
        # Beräkna negativ acceleration från vattnet
        self.break_x = self.size * self.change_x * math.fabs(self.change_x) / self.mass
        self.break_y = self.size * self.change_y * math.fabs(self.change_y) / self.mass
