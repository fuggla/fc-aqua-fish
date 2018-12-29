
import arcade, random, math
from vars import TICK_RATE
from fish_names import fish_names, fish_names_length

class FishSprite(arcade.Sprite):
    def __init__(self):
        # Anropa Sprite konstruktor
        super().__init__()

        # Definiera hastighet och acceleration
        self.change_x = 0       # x_hastighet
        self.change_y = 0       # y_hastighet
        self.acc_x = 0          # positiv x_acceleration
        self.acc_y = 0          # negativ y_acceleration
        self.break_x = 0        # negativ x_acceleration
        self.break_y = 0        # negativ y_acceleration

        self.name_gender = fish_names[random.randrange(fish_names_length)]

        self.health = 100000
        self.isalive = True
        self.eat_speed = 0
        self.iseating = 0
        self.tick_rate = TICK_RATE

    def move_calc(self):
        # Hastigheten är tidigare hastighet plus positiv acceleration minus negativ acceleration
        # Här ska programmets framerate in stället för 30
        self.change_x = self.change_x + (self.acc_x - self.break_x) / self.tick_rate
        self.change_y = self.change_y + (self.acc_y - self.break_y) / self.tick_rate

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

    def check_edge(self):
        # Kolla om fisken är nära kanten, styr in dem mot mitten och stressa upp den
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

    def eat_food(self, carrot, chew):
        # Sätt vatiabel så att fiskarna vet att de äter
        if self.iseating <= 10:
            self.iseating += 1
        self.health += 1

        # Beräkna vinkel mot moroten fisken äter
        ang_rad = math.atan2((carrot.center_y - self.center_y), (carrot.center_x - self.center_x))
        ang_deg = math.degrees(ang_rad)     # omvandla till degrees
        self.angle = ang_deg
        self.animate_eat_food()

        carrot.food_value -= chew               # Fiskarna äter moroten
        if carrot.food_value <= 750:
            carrot.texture = carrot.texture_carrot2
        if carrot.food_value <= 500:
            carrot.texture = carrot.texture_carrot3
        if carrot.food_value <= 250:
            carrot.texture = carrot.texture_carrot4
        if carrot.food_value <= 0:              # När moroten är slut försvinner den
            carrot.kill()

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


