
import arcade, random, math
from vars import TICK_RATE

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

    def eat_food(self, carrot):
        ang_rad = math.atan((carrot.center_y - self.center_y) / (carrot.center_x - self.center_x))
        ang_deg = math.degrees(ang_rad)
        if self.whichtexture < 20:
            ang_deg += 180
        self.angle = ang_deg
        carrot.food_value -= 1
        if carrot.food_value == 0:
            carrot.kill()
            self.angle = 0

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