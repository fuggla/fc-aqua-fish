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

VERSION = 0.3
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
        self.button_list = None
        self.all_sprite_list = None

        #self.player_list = None

    def setup(self):
        # Alla arcade sprites och sprites_list här
        self.pfish_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        # Skapa lila fiskar
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(SPRITE_SCALING_PFISH, SCREEN_WIDTH, SCREEN_HEIGHT, self.carrot_list)
            self.pfish_list.append(pfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(pfish)                      # och i totallistan

        # Skapa en lista på knappar
        self.button_list = []
        self.button_list.append(Button(30, 585, 50, 20, "Exit", 11, arcade.window_commands.close_window))
        self.button_list.append(Button(115, 585, 100, 20, "New Game", 11, self.setup))
        self.button_list.append(Button(225, 585, 100, 20, "Do it!", 11, self.do_it))

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

        # Rita alla knappar
        if self.is_paused():
            for button in self.button_list:
                button.draw()

        # Call draw() on all your sprite lists below

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        if self.is_playing():
            self.all_sprite_list.update()

            """ Skapa en morot med sannolikheten 1 på 1000 varje frame """
            if random.randrange(500) < 1:
                carrot = CarrotSprite(SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT)
                self.carrot_list.append(carrot)
                self.all_sprite_list.append(carrot)

            """ Ta bort morötter som ramlat ner """
            for carrot in self.carrot_list:
                if carrot.top < 0:
                    carrot.kill()

            """ Ta bort morötter som fiskarna äter upp """
            for fish in self.pfish_list:
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                for carrot in hit_list:
                    carrot.kill()

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
            self.toggle_pause()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Kolla om vi klickat på någon knapp
        if self.is_paused():
            for b in self.button_list:
                b.on_mouse_release(x, y)

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
