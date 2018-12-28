import arcade, random, math
from classes.fish import FishSprite
from vars import SPRITE_SCALING_BFISH, SCREEN_WIDTH, SCREEN_HEIGHT

# Klass för lila fiskar (Purple_fish)
class PfishSprite(FishSprite):
    def __init__(self, carrot_list):
        # Anropa Sprite konstruktor
        super().__init__()