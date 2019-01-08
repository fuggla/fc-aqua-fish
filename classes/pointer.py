import arcade


class Pointer(arcade.Sprite):
# Klass för muspekare
    def __init__(self):
        # Anropa superklassen
        super().__init__()

        self.center_x = None
        self.center_y = None

        # Ladda in texture för att peka och för att hålla
        img = "assets/images/pointer"
        self.texture_point = arcade.load_texture(f"{img}/point.png")
        self.texture_grab = arcade.load_texture(f"{img}/grab.png")

        self.texture = self.texture_point
