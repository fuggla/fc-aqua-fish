import arcade, random, math
from classes.fish import FishSprite
from vars import SPRITE_SCALING_BFISH, SCREEN_WIDTH, SCREEN_HEIGHT

# Klass för små blå fiskar (blue_fish)
class BfishSprite(FishSprite):
    def __init__(self, carrot_list):
        # Anropa Sprite konstruktor
        super().__init__()

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT