
import random, math

""" 
Klass för alla rörelser fiskarna kan göra.
Alla metoder som behandlar rörelse ligger här
"""


class FishMove:

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

    def hook_move(self):
        # Räkna fiskens koordinater då den fastnat på kroken
        bite_x = self.hook.center_x + self.hook_bite_pos_diff[0]
        bite_y = self.hook.center_y + self.hook_bite_pos_diff[1]
        dist_tot = self.width * 0.4
        self.center_x = bite_x
        self.center_y = bite_y - dist_tot
        self.angle = 90
        self.set_texture(2)

        if self.bottom > self.sh:
            self.kill()

    def move_calc(self):
        # Hastigheten är tidigare hastighet plus positiv acceleration minus negativ acceleration
        # Här ska programmets framerate in stället för 30
        if self.dragged:
            self.change_x = 0
            self.change_y = 0
        else:
            self.change_x = self.change_x + (self.acc_x - self.break_x) / self.tick_rate
            self.change_y = self.change_y + (self.acc_y - self.break_y) / self.tick_rate

        # Fiskarna plaskar till när de faller tillbaka
        if self.change_y < 0 and self.bottom > self.sh:
            self.change_y = -30

        # Helt annat ifall fisken fastnat på kroken
        if self.hook:
            self.hook_move()

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
            partner.kiss_amount += 1
            self.kiss_amount += 1
            partner.partner = None
            self.partner = None

    def random_move(self):
        # Ändra accelerationen slumpartat
        self.acc_x = (random.random() * 2 - 1) * self.finforce / self.mass
        self.acc_y = (random.random() * 2 - 1) * self.finforce / self.mass

    def shoal_move(self):
        """ Hämta in koordinater och hastihet från närmsta två blue_small_fish """
        if len(self.bfish_list) > 1:

            dist1 = 1000000000      # variable där avstånet (i kvadrat) till närmaste bfish sparas
            dist2 = 1000000000

            fish1 = 0               # index för närmaste bfish
            fish2 = 0               # index för näst närmaste bfish

            index = 0

            # Stega igenom alla fiskar och spara index och avstånd om de är närmast eller näst närmast
            for fish in self.bfish_list:
                if fish.center_x == self.center_x and fish.center_y == self.center_y:   # Räkna bort sig själv
                    pass
                elif ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2) < dist1:
                    dist1 = ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2)
                    fish1 = index
                elif ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2) < dist2:
                    dist2 = ((fish.center_x - self.center_x) ** 2 + (fish.center_y - self.center_y) ** 2)
                    fish2 = index
                index += 1
            if len(self.bfish_list) == 2:
                # Spara x- & y-positioner för närmaste och näst närmaste fisk
                midpos_x = self.bfish_list[fish1].center_x
                midpos_y = self.bfish_list[fish1].center_y


            elif len(self.bfish_list) >= 3:
                # Spara x- & y-positioner för närmaste och näst närmaste fisk
                pos1_x = self.bfish_list[fish1].center_x
                pos1_y = self.bfish_list[fish1].center_y

                pos2_x = self.bfish_list[fish2].center_x
                pos2_y = self.bfish_list[fish2].center_y

                # Beräkna medelvärde för dessa positioner
                midpos_x = (pos1_x + pos2_x) / 2
                midpos_y = (pos1_y + pos2_y) / 2

            # Beräkna vinkel mot medelvärdet av positionerna och accelerera ditåt
            ang = math.atan2((midpos_y - self.center_y), (midpos_x - self.center_x))
            shoal_speed = random.random() * self.finforce / self.mass
            self.acc_x = shoal_speed * math.cos(ang)
            self.acc_y = shoal_speed * math.sin(ang)


