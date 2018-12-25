"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types
from classes.state import State
from classes.button import Button
from classes.purple_fish import PfishSprite
from classes.carrot import CarrotSprite
from classes.window import Window

VERSION = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPRITE_SCALING_PFISH = 0.1
PFISH_NUMBER = 5

SPRITE_SCALING_CARROT = 0.3

# Test att ändra två filer samtidigt

class MyGame(arcade.Window, State):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        # BLUE_SAPPHIRE eller BLUE_YONDER, båda är rätt snygga
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        self.frame_count = 0

        # If you have sprite lists, you should create them here
        self.pfish_list = None
        self.carrot_list = None
        self.all_sprite_list = None
        self.window_list = None

        #self.player_list = None

    def setup(self):
        # Alla arcade sprites och sprites_list här
        self.pfish_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        # Skapa lila fiskar
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(SPRITE_SCALING_PFISH, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.pfish_list.append(pfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(pfish)                      # och i totallistan

        # Skapa en morot
        carrot = CarrotSprite(SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)

        # Skapa fönster
        self.window_list = []

        # Skapa huvudmeny att visa med escape
        self.main_menu = Window(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 90, "Aqua Fish")
        self.main_menu.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        self.main_menu.add_button(50, 10, 180, 30, "Exit", 11, arcade.window_commands.close_window)
        self.window_list.append(self.main_menu)

        # Setup klar
        self.state = "playing"

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.all_sprite_list.draw()

        # Rita bara huvudmeny om vi har pausat spelet
        if self.is_paused():
            self.main_menu.draw()
        # Call draw() on all your sprite lists below

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        if self.is_playing():
            self.all_sprite_list.update()

        self.frame_count += 1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

        # key är en int
        # Se: http://arcade.academy/arcade.key.html
    def on_key_release(self, key, key_modifiers):
        # Avsluta AL
        if (key == arcade.key.Q):
            arcade.window_commands.close_window()
        # Starta om
        elif (key == arcade.key.R):
            self.setup()
        elif (key == arcade.key.ESCAPE):
            self.main_menu.open()
            self.toggle_pause()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        for w in self.window_list:
            if w.is_dragged():
                w.move(delta_x, delta_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        for w in self.window_list:
            if w.is_open():
                self.main_menu.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Kolla om vi klickat på någon knapp i huvudmenyn
        for w in self.window_list:
            if w.is_open():
                self.main_menu.on_mouse_release(x, y)

    def do_it(self):
        global PFISH_NUMBER
        PFISH_NUMBER = PFISH_NUMBER * 25
        self.setup()

def main():
    print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
