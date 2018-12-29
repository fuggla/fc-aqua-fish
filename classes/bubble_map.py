# Class Bubble_map
# Ritar en bild med X antal bubblor
# Bilden flytta uppåt på skärmen i en loop
# Flyttas ner när den är utanför skärmen

import arcade,random
from vars import SCREEN_WIDTH, SCREEN_HEIGHT

class Bubble_map():

    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, amount=50, size=3, border_width=1, color=(255,255,255,random.randrange(32, 128)), speed=50):

        # Höjd / Grundhastighet / nuvarande hastighet
        self.h = h
        self.speed = speed
        self.base_speed = speed

        # Rita alla bubblor i lista
        self.bubble_list = arcade.ShapeElementList()
        #self.bubble_list.append(arcade.create_rectangle_outline((w/2), (h/2), w, h, (random.randrange(255),random.randrange(255),random.randrange(255)), border_width * 2))
        for b in range(0, amount):
            radius = random.randrange(1, size)
            self.bubble_list.append(arcade.create_ellipse_outline(random.randrange(w), random.randrange(h), radius, radius, color, border_width))

        # Kalla direkt på objektet för att rita listan
        self.draw = self.bubble_list.draw

        # Slumpa fram en synlig startposition och hastighet
        self.bubble_list.center_y = random.randrange(-h, h)
        self.new_speed()
        
    # Flytta ner under skärmen och ändra till ny hastighet
    def move_down(self):
        self.bubble_list.center_y = -self.h

    def new_speed(self):
        self.speed = random.randrange(self.base_speed * 0.5, self.base_speed * 1.5)
        
    # Flyt uppåt och flytta ner vid behov
    def update(self, dt):
        self.bubble_list.center_y += self.speed * dt
        if (self.bubble_list.center_y > self.h - 50):
            self.move_down()
            self.new_speed()
