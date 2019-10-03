# Class Bubble_map
# Ritar en bild med X antal bubblor
# Bilden flytta uppåt på skärmen i en loop
# Flyttas ner när den är utanför skärmen

from random import randrange
from arcade import ShapeElementList, create_ellipse_outline, create_rectangle_outline
from vars import SCREEN_WIDTH, SCREEN_HEIGHT

class Bubble_map():

    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, amount=50, size=3, border_width=1, color=(255,255,255, randrange(64, 192)), speed=50):

        # Höjd / Grundhastighet / nuvarande hastighet
        self.h = h
        self.speed = speed
        self.base_speed = speed

        # Rita alla bubblor i lista
        self.bubble_list = ShapeElementList()
        for b in range(0, amount):
            radius = randrange(1, size)
            self.bubble_list.append(create_ellipse_outline(randrange(w), randrange(h), radius, radius, color, border_width))

        # Kalla direkt på objektet för att rita listan
        self.draw = self.bubble_list.draw

        # Slumpa fram en synlig startposition och hastighet
        self.bubble_list.center_y = randrange(-h, h)
        self.new_speed()
        
    # Flytta ner under skärmen
    def move_down(self):
        self.bubble_list.center_y = -self.h

    # Slumpa ny hastiget
    def new_speed(self):
        self.speed = randrange(self.base_speed * 0.5, self.base_speed * 1.5)
        
    # Flyt uppåt och flytta ner vid behov
    def update(self, dt):
        self.bubble_list.center_y += self.speed * dt
        if (self.bubble_list.center_y > self.h - 50):
            self.move_down()
            self.new_speed()
