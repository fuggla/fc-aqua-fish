
import math

""" 
Klass för alla fiskarnas animationer.
Alla metoder som behandlar animationer ligger här
"""


class FishAnimate:
    def animate(self):
        # Animering av fiskarna
        if self.iseating == 0:

            if not self.is_hooked:
                self.angle = 0
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y)) / self.finforce + 1))

            # Vänd dem i x-hastighetens riktning
            if self.change_x < 0 and not (self.whichtexture == 11 or self.whichtexture == 12):
                self.set_texture(0)
                self.whichtexture = 11
            if self.change_x > 0 and not (self.whichtexture == 21 or self.whichtexture == 22):
                self.set_texture(2)
                self.whichtexture = 21
            # "self.whichtexture = 11" betyder "left texture 1"
            # "self.whichtexture = 22" betyder "right texture 2"

            # Animation riktad åt vänster
            if self.frame_count % self.findelay == 0 and self.whichtexture == 11:
                self.set_texture(1)
                self.whichtexture = 12
            elif self.frame_count % self.findelay == 0 and self.whichtexture == 12:
                self.set_texture(0)
                self.whichtexture = 11
            # Animation riktad åt höger
            if self.frame_count % self.findelay == 0 and self.whichtexture == 21:
                self.set_texture(3)
                self.whichtexture = 22
            elif self.frame_count % self.findelay == 0 and self.whichtexture == 22:
                self.set_texture(2)
                self.whichtexture = 21

    def animate_eat_food(self):

        if -90 < self.angle < 90:
            # Ätanimation då fisken är riktad åt höger
            if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18 or self.whichtexture == 22:
                self.set_texture(0)
                self.whichtexture = 21

            if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                self.set_texture(5)
                self.whichtexture = 28
            elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 28:
                self.set_texture(2)
                self.whichtexture = 21

        else:
            # Ätanimation då fisken är riktad åt vänster
            if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28 or self.whichtexture == 12:
                self.set_texture(0)
                self.whichtexture = 11

            if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                self.set_texture(4)
                self.whichtexture = 18
            elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 18:
                self.set_texture(0)
                self.whichtexture = 11
            self.angle += 180

    def animate_hunt(self):
        # Animering av jakten
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y))/self.finforce + 1))

            # Vänd dem i riktning mot bytet
            if -90 < self.angle < 90:
                # Ätanimation då fisken är riktad åt höger
                if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18:
                    self.set_texture(6)
                    self.whichtexture = 21

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                    self.set_texture(7)
                    self.whichtexture = 22
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 22:
                    self.set_texture(6)
                    self.whichtexture = 21

            else:
                # Ätanimation då fisken är riktad åt vänster
                if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28:
                    self.set_texture(4)
                    self.whichtexture = 11

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                    self.set_texture(5)
                    self.whichtexture = 12
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 12:
                    self.set_texture(4)
                    self.whichtexture = 11
                self.angle += 180

    def animate_love(self):
        # Animering rörelse mot partner
            # Ändra fenfrekvens utifrån totalacceleration
            self.findelay = int(self.findelay_base / ((math.fabs(self.acc_x) + math.fabs(self.acc_y))/self.finforce + 1))

            # Vänd  dem i riktning mot partnern
            if -90 < self.angle < 90:
                # Ätanimation då fisken är riktad åt höger
                if self.whichtexture == 11 or self.whichtexture == 12 or self.whichtexture == 18 or self.whichtexture == 28:
                    self.set_texture(2)
                    self.whichtexture = 21

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 21:
                    self.set_texture(3)
                    self.whichtexture = 22
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 22:
                    self.set_texture(2)
                    self.whichtexture = 21

            else:
                # Ätanimation då fisken är riktad åt vänster
                if self.whichtexture == 21 or self.whichtexture == 22 or self.whichtexture == 28 or self.whichtexture == 18:
                    self.set_texture(0)
                    self.whichtexture = 11

                if self.frame_count % self.eat_speed == 0 and self.whichtexture == 11:
                    self.set_texture(1)
                    self.whichtexture = 12
                elif self.frame_count % self.eat_speed == 0 and self.whichtexture == 12:
                    self.set_texture(0)
                    self.whichtexture = 11
                self.angle += 180
