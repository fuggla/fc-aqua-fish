
import arcade, random, math, csv
from vars import TICK_RATE, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO

# Läs fisknamn från names.csv
fish_names = []
with open('names.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        fish_names.append([row[1], row[0]])
fish_names_length = len(fish_names)

class FishSprite(arcade.Sprite):
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

        self.health = random.randint(10000, 15000)
        self.base_health = self.health
        self.hunting_spirit = 0
        self.isalive = True
        self.disturbed = False
        self.eat_speed = 0
        self.iseating = 0
        self.tick_rate = TICK_RATE

        # För kommunikation ut från objekt
        self.event = event or None

        # Fiskarnas namn, kön och sexualitet
        self.name_gender = fish_names[random.randrange(fish_names_length)]
        self.partner = None
        self.pregnant = False
        self.ready_to_lay_egg = False
        self.kiss_spirit = 0
        self.egg_postition = [0, 0]

        rand = random.random()
        # Damfisk
        if self.name_gender[1] == "f":
            if rand < 0.95:
                self.attraction = "m"
            elif 0.98 >= rand >= 0.95:
                self.attraction = "f"
            else:
                self.attraction = "open minded"
        # Herrfisk
        if self.name_gender[1] == "m":
            if rand < 0.95:
                self.attraction = "f"
            elif 0.98 >= rand >= 0.95:
                self.attraction = "m"
            else:
                self.attraction = "open minded"
        # Genderfluid
        if self.name_gender[1] == "g":
            if rand < 0.2:
                self.attraction = "f"
            elif 0.2 >= rand >= 0.4:
                self.attraction = "m"
            else:
                self.attraction = "open minded"

    def move_calc(self):
        # Hastigheten är tidigare hastighet plus positiv acceleration minus negativ acceleration
        # Här ska programmets framerate in stället för 30
        self.change_x = self.change_x + (self.acc_x - self.break_x) / self.tick_rate
        self.change_y = self.change_y + (self.acc_y - self.break_y) / self.tick_rate

    def health_calc(self):

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

    def water_res(self):
        # Beräkna negativ acceleration från vattnet
        self.break_x = self.size * self.change_x * math.fabs(self.change_x) / self.mass
        self.break_y = self.size * self.change_y * math.fabs(self.change_y) / self.mass

    def random_move(self):
        # Ändra accelerationen slumpartat
        self.acc_x = (random.random() * 2 - 1) * self.finforce / self.mass
        self.acc_y = (random.random() * 2 - 1) * self.finforce / self.mass

    def chase_food(self):
        # metod för att vända sig mot och accelerera mot mat
        if self.food_objects:
            food_cor = []
            # Spara alla morätternas koordinater i food_cor
            for food in self.food_objects:
                food_cor.append([food.center_x, food.center_y])

            # Beräkna avståndet till maten som är närmast
            nerest_carrot = [(food_cor[0][0] - self.center_x), (food_cor[0][1] - self.center_y)]
            for food in food_cor:
                if ((food[0] - self.center_x) ** 2 + (food[1] - self.center_y) ** 2) < (
                        nerest_carrot[0] ** 2 + nerest_carrot[1] ** 2):
                    nerest_carrot = [(food[0] - self.center_x), (food[1] - self.center_y)]

            # Beräkna vinkel mot maten
            ang = math.atan2(nerest_carrot[1], nerest_carrot[0])
            foodspeed = random.random() * self.finforce / self.mass
            self.acc_x = foodspeed * math.cos(ang)
            self.acc_y = foodspeed * math.sin(ang)

    def chase_fish(self):
        # metod för att vända sig mot och accelerera mot mat
        if self.food_fish_list:
            food_cor = []
            # Spara alla morätternas koordinater i food_cor
            for food in self.food_fish_list:
                food_cor.append([food.center_x, food.center_y])

            # Beräkna avståndet till maten som är närmast
            nerest_fish = [(food_cor[0][0] - self.center_x), (food_cor[0][1] - self.center_y)]
            for food in food_cor:
                if ((food[0] - self.center_x) ** 2 + (food[1] - self.center_y) ** 2) < (
                        nerest_fish[0] ** 2 + nerest_fish[1] ** 2):
                    nerest_fish = [(food[0] - self.center_x), (food[1] - self.center_y)]

            # Beräkna vinkel mot maten
            ang = math.atan2(nerest_fish[1], nerest_fish[0])
            self.angle = math.degrees(ang)
            foodspeed = random.random() * self.finforce / self.mass
            self.acc_x = foodspeed * math.cos(ang)
            self.acc_y = foodspeed * math.sin(ang)

    def find_partner(self, possible_partner_list):
        # metod för att hitta en villig partner
        # Spara alla möjliga partners koordinater i patner_list
        # Loopen letar efter villiga partners med kön som fisken attraheras av
        if possible_partner_list:
            attraction_list = []
            for partner in possible_partner_list:
                if self == partner:
                    pass
                elif self.attraction == "m" and partner.name_gender[1] == "m" and partner.kiss_spirit > 0 and not partner.partner:
                    attraction_list.append(partner)
                elif self.attraction == "f" and partner.name_gender[1] == "f" and partner.kiss_spirit > 0 and not partner.partner:
                    attraction_list.append(partner)
                elif self.attraction == "open minded" and partner.kiss_spirit > 0 and not partner.partner:
                    attraction_list.append(partner)

            if attraction_list:
                # Kolla vilka möjliga partners fisken attraheras av som attraheras av fisken
                partner_list = []
                for partner in attraction_list:
                    if partner.attraction == "m" and self.name_gender[1] == "m":
                        partner_list.append(partner)
                    elif partner.attraction == "f" and self.name_gender[1] == "f":
                        partner_list.append(partner)
                    elif self.attraction == "open minded":
                        partner_list.append(partner)

                # I slutändan är det omöjligt att veta vad som får två fiskar att bli kära i varandra
                if partner_list:
                    partner = random.choice(partner_list)

                    # Spara kärleken i variabeln "partner"
                    self.partner = partner
                    partner.partner = self

    def move_to_partner_kiss(self, partner):

        # Beräkna vinkel och avstång mot partner
        ang = math.atan2((partner.center_y - self.center_y), (partner.center_x - self.center_x))
        self.angle = math.degrees(ang)
        dist_square = (partner.center_x - self.center_x) ** 2 + (partner.center_y - self.center_y) ** 2


        if self.type == "bfish":
            break_dist = 300
            stop_fak = 0.85
        elif self.type == "pfish":
            break_dist = 400
            stop_fak = 0.6
        elif self.type == "shark":
            break_dist = 700
            stop_fak = 0.8

        if dist_square < break_dist ** 2:
            kiss_speed = self.finforce * (dist_square / break_dist ** 2) / self.mass
        else:
            kiss_speed = self.finforce / self.mass

        # Accelerera mot partner
        self.acc_x = kiss_speed * math.cos(ang)
        self.acc_y = kiss_speed * math.sin(ang)

        # Om de möts så pussas de.
        if (self.center_x - partner.center_x) ** 2 + (self.center_y - partner.center_y) ** 2 < self.width ** 2 * stop_fak:
            self.kiss_spirit = 0
            partner.kiss_spirit = 0
            self.health = self.base_health
            partner.health = partner.base_health
            # "male" + "female" kan ge graviditet med 70 % chans
            if self.name_gender[1] == "f" and partner.name_gender[1] == "m" and random.random() <= 0.7:
                self.pregnant = True
                self.get_lay_egg_position()
            if self.name_gender[1] == "m" and partner.name_gender[1] == "f" and random.random() <= 0.7:
                partner.pregnant = True
                partner.get_lay_egg_position()
            # Fiskarna har inga långa förhållanden efter de pussats
            partner.partner = None
            self.partner = None

    def get_lay_egg_position(self):
        # Metod för att hitta en plats där fisken kan lägga ägg
        self.egg_postition[0] = random.randrange(int(self.sw * 0.1), int(self.sw * 0.9))
        self.egg_postition[1] = random.randrange(int(self.sh * self.sr * 0.3), int(self.sh * self.sr))

    def move_lay_egg_position(self):
        # Metod för att hitta en plats där fisken kan lägga ägg
        # Beräkna vinkel och avstånd i kvadrat mot positionen
        ang = math.atan2(self.egg_postition[1] - self.center_y, self.egg_postition[0] - self.center_x)
        self.angle = math.degrees(ang)
        dist_square = (self.egg_postition[0] - self.center_x) ** 2 + (self.egg_postition[1] - self.center_y) ** 2

        if dist_square < 200 ** 2:
            egg_speed = self.finforce * (dist_square / 200 ** 2) / self.mass
        else:
            egg_speed = self.finforce / self.mass

        self.acc_x = egg_speed * math.cos(ang)
        self.acc_y = egg_speed * math.sin(ang)

        # Om fisken är nära rätt position kan den lägga ägg
        if dist_square < 50 ** 2:
            self.ready_to_lay_egg = True

    def flee_from_close_fish(self):
        # metod för att vända sig mot och accelerera mot mat
        if self.hunter_fish_list:
            hunter_cor = []
            # Spara alla morätternas koordinater i hunter_cor
            for hunter in self.hunter_fish_list:
                hunter_cor.append([hunter.center_x, hunter.center_y])

            # Beräkna avståndet till maten som är närmast
            nerest_hunter = [(hunter_cor[0][0] - self.center_x), (hunter_cor[0][1] - self.center_y)]
            for hunter in hunter_cor:
                if ((hunter[0] - self.center_x) ** 2 + (hunter[1] - self.center_y) ** 2) < (
                        nerest_hunter[0] ** 2 + nerest_hunter[1] ** 2):
                    nerest_hunter = [(hunter[0] - self.center_x), (hunter[1] - self.center_y)]

            # Om närmaste jägaren är nära så beräkna vinkel dit och simma så snabbt en kan
            if (nerest_hunter[0] ** 2 + nerest_hunter[1] ** 2) < (250 ** 2):
                ang = math.atan2(nerest_hunter[1], nerest_hunter[0]) + 3.14
                flee_speed = random.random() * self.finforce / self.mass
                self.acc_x = flee_speed * math.cos(ang)
                self.acc_y = flee_speed * math.sin(ang)

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

        food.food_value -= chew               # Fiskarna äter moroten
        if food.food_value <= 750:
            food.texture = food.texture_food2
        if food.food_value <= 500:
            food.texture = food.texture_food3
        if food.food_value <= 250:
            food.texture = food.texture_food4
        if food.food_value <= 0:              # När moroten är slut försvinner den
            food.kill()


    def eat_fish(self, prey):
        if self.hunting_spirit > 0:
            self.health += 10000
            self.iseating = 10

            self.hunting_spirit = 0
            if -90 < self.angle < 90:
                self.texture = self.texture_right1
            else:
                self.texture = self.texture_left1

            prey.kill()
            self.event.put(self.get_name() + " ate " + prey.get_name())

    def die(self):
        self.isalive = False
        self.acc_x = 0
        self.acc_y = .1
        if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
            self.angle = 180
            self.texture = self.texture_right1
        if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
            self.angle = 180
            self.texture = self.texture_left1

    def animate_eat_food(self):

        if -90 < self.angle < 90:
            # Ätanimation då fisken är riktad åt höger
            if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
                self.texture = self.texture_right1
                self.whichtexture = 21

            if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                self.texture = self.texture_right8
                self.whichtexture = 28
            elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 28:
                self.texture = self.texture_right1
                self.whichtexture = 21

        else:
            # Ätanimation då fisken är riktad åt vänster
            self.angle += 180
            if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
                self.texture = self.texture_left1
                self.whichtexture = 11

            if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                self.texture = self.texture_left8
                self.whichtexture = 18
            elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 18:
                self.texture = self.texture_left1
                self.whichtexture = 11

    def animate(self):
        # Animering av fiskarna
        if self.iseating == 0:

            self.angle = 0
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y)) / self.finforce + 1))

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

    def animate_hunt(self):
        # Animering av jakten
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y))/self.finforce + 1))

            # Vänd dem i riktning mot bytet
            if -90 < self.angle < 90:
                # Ätanimation då fisken är riktad åt höger
                if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
                    self.texture = self.texture_right_eat1
                    self.whichtexture = 21

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                    self.texture = self.texture_right_eat2
                    self.whichtexture = 22
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 22:
                    self.texture = self.texture_right_eat1
                    self.whichtexture = 21

            else:
                # Ätanimation då fisken är riktad åt vänster
                self.angle += 180
                if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
                    self.texture = self.texture_left_eat1
                    self.whichtexture = 11

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                    self.texture = self.texture_left_eat2
                    self.whichtexture = 12
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 12:
                    self.texture = self.texture_left_eat1
                    self.whichtexture = 11

    def animate_love(self):
        # Animering rörelse mot partner
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y))/self.finforce + 1))

            # Vänd dem i riktning mot partnern
            if -90 < self.angle < 90:
                # Ätanimation då fisken är riktad åt höger
                if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
                    self.texture = self.texture_right1
                    self.whichtexture = 21

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                    self.texture = self.texture_right2
                    self.whichtexture = 22
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 22:
                    self.texture = self.texture_right1
                    self.whichtexture = 21

            else:
                # Ätanimation då fisken är riktad åt vänster
                self.angle += 180
                if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
                    self.texture = self.texture_left1
                    self.whichtexture = 11

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                    self.texture = self.texture_left2
                    self.whichtexture = 12
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 12:
                    self.texture = self.texture_left1
                    self.whichtexture = 11

    def get_name(self):
        return self.name_gender[0]
