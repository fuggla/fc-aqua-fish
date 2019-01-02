from vars import SCREEN_HEIGHT, SCREEN_WIDTH
from arcade import arcade.color, arcade.draw


# Hantering av game state
class Fade():
    
    def __init__(self, color=(0,0,0,255)):
        self.color = color
        self.x = 0
        self.y = 0
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
    def fade(self, color):
        self.color = color
        self.fade = true

    def update(self, dt):
        pass

    def draw(self, dt):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
