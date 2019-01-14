import arcade
from vars import SCALING_POINTER

class Pointer(arcade.Sprite):
# Klass för muspekare
    def __init__(self):
        # Anropa superklassen
        super().__init__()

        # Ladda in texture för att peka och för att hålla
        img = "assets/images/pointer/"
        self.textures = []
        self.append_texture(arcade.load_texture(f"{img}point.png", scale=SCALING_POINTER))
        self.append_texture(arcade.load_texture(f"{img}grab.png", scale=SCALING_POINTER))
        self.set_texture(0)

        # Allt jox är för att fingret ska hamna på samma plats som orginalmusens "pekare"
        self.xmod = self.width*0.3
        self.ymod = self.height*0.5

    # Om musen håller i ett fönster så byt textur
    def grab(self):
        self.set_texture(1)  # Om musen håller i ett fönster så byt textur

    # Byt tillbaka till vanliga texturen
    def point(self):
        self.set_texture(0)

    # Flytta muspekaren
    def on_mouse_motion(self, x, y):
        self.set_position(x - self.xmod, y - self.ymod)
