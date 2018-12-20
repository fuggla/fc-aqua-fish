"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random

VERSION = 0.1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPRITE_SCALING_PFISH = 0.1
PFISH_NUMBER = 3

# Test att ändra två filer samtidigt

class MyGame(arcade.Window):
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

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.pfish_list = None                  # Skapa en lista där lila fiskar kommer simma
        self.button_list = None                 # (Jag fattar inte varför den måste in här)

        #self.player_list = None

    def setup(self):
        # Create your sprites and sprite lists here

        self.pfish_list = arcade.SpriteList()   # Listan blir en arcadelista
        # Loop som skapar "PFISH_NUMBER" många lila fiskar
        for i in range(PFISH_NUMBER):
            pfish = arcade.Sprite("images/purple_fish1.png",SPRITE_SCALING_PFISH)
            # Detta placerar dem random inom 90 % från mitten
            pfish.center_x = random.randrange(SCREEN_WIDTH*0.8)+SCREEN_WIDTH*0.1
            pfish.center_y = random.randrange(SCREEN_HEIGHT*0.8)+SCREEN_HEIGHT*0.1
            self.pfish_list.append(pfish)           # Lägg till fiskarna i fisklistan

        # Skapa en lista på knappar
        self.button_list = []
        self.button_list.append(Button(30, 585, 50, 20, "Exit"))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.pfish_list.draw()

        # Rita bara knapp 1 just nu (ändra till loop sen)
        self.button_list[0].draw()

        # Call draw() on all your sprite lists below

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

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
        """
        Called when a user releases a mouse button.
        """
        pass

class Button():

    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    # Rita knapp
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.LIGHT_GRAY)

def main():
    print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
