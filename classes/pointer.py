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

        self.is_visable = True
        self.frames = 0
        self.timer = 0

    def update(self):
        # Öka timer varje sekund
        if self.frames % 60 == 0 and not self.check_move():
            self.timer += 1
        self.frames += 1

        print(self.frames)
        if self.timer >= 4:
            self.is_visable = False

        if self.check_move():
            self.is_visable = True
            self.timer = 0

        super().update()

    def grab(self):
        # Om musen håller i ett fönster så byt textur
        self.set_texture(1)  # Om musen håller i ett fönster så byt textur

    def point(self):
        # Byt tillbaka till vanliga texturen
        self.set_texture(0)

    def on_mouse_motion(self, x, y):
        # Flytta muspekaren
        self.set_position(x - self.xmod, y - self.ymod)

    def hide_pointer(self):
        self.is_visable = False

    def show_pointer(self):
        self.is_visable = True

    def check_move(self):
        if self.center_x == self.last_center_x and self.center_y == self.last_center_y:
            return False
        else:
            return True
