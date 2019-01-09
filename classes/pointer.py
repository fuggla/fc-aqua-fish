import arcade
from vars import SCALING_POINTER

class Pointer(arcade.Sprite):
# Klass för muspekare
    def __init__(self):
        # Anropa superklassen
        super().__init__()

        # Ladda in texture för att peka och för att hålla
        img = "assets/images/pointer"
        self.texture_point = arcade.load_texture(f"{img}/point.png", scale=SCALING_POINTER)
        self.texture_grab = arcade.load_texture(f"{img}/grab.png", scale=SCALING_POINTER )

        self.texture = self.texture_point

    # Om musen håller i ett fönster så byt textur
    def grab(self):
        self.texture = self.texture_grab  # Om musen håller i ett fönster så byt textur

    # Byt tillbaka till vanliga texturen
    def point(self):
        self.texture = self.texture_point
