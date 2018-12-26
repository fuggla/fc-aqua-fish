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
from vars import *

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

        # FPS
        self.fps = 0
        self.tick = 0
        self.delta_count = 0
        self.show_fps = False
        
        #self.player_list = None

    def setup(self):
        # Alla arcade sprites och sprites_list här
        self.pfish_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        # Skapa lila fiskar
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.carrot_list)
            self.pfish_list.append(pfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(pfish)                      # och i totallistan

        # Skapa fönster
        self.window_list = []

        # Skapa meny för att interagera med akvariet
        self.interaction_menu = Window(SCREEN_WIDTH / 2, 30, 390, 50, "Store")
        self.interaction_menu.add_button(10, 10, 180, 30, "Buy Fish", 11, self.add_fish)
        self.interaction_menu.add_button(10, 200, 180, 30, "Buy FPS counter", 11, self.enable_fps)
        self.window_list.append(self.interaction_menu)
        self.interaction_menu.open()

        # Skapa huvudmeny att visa med escape
        self.main_menu = Window(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 130, "Aqua Fish")
        self.main_menu.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        self.main_menu.add_button(50, 10, 180, 30, "Open Store", 11, self.interaction_menu.open)
        self.main_menu.add_button(90, 10, 180, 30, "Exit", 11, arcade.window_commands.close_window)
        self.window_list.append(self.main_menu)

        # Setup klar
        self.play()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Rita ut sandbotten
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT * SAND_RATIO / 2, SCREEN_WIDTH,
                                     SCREEN_HEIGHT * SAND_RATIO, arcade.color.SAND)
        arcade.draw_rectangle_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT * SAND_RATIO / 2, SCREEN_WIDTH-2,
                                     SCREEN_HEIGHT * SAND_RATIO-2, arcade.color.BLACK, 3)

        self.all_sprite_list.draw()

        # Rita bara huvudmeny om vi har pausat spelet
        if self.is_paused():
            self.main_menu.draw()

        for w in self.window_list:
            w.draw()
        # Call draw() on all your sprite lists below

        if self.show_fps:
            arcade.draw_text(str(self.fps), 10, SCREEN_HEIGHT - 10, arcade.color.BLACK, font_size=8, width=10, align="left", anchor_x="center", anchor_y="center")

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
                carrot = CarrotSprite(SPRITE_SCALING_CARROT, SCREEN_WIDTH, SCREEN_HEIGHT, SAND_RATIO)
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

        if self.show_fps:
            self.fps = int(1 / delta_time)
        """
        if self.show_fps:
            self.tick += 1
            self.delta_count += delta_time
            if self.delta_count >= 1:
                self.fps = self.tick
                self.delta_count = 0
                self.tick = 0
        """

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
                w.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Kolla om vi klickat på någon knapp i huvudmenyn
        for w in self.window_list:
            if w.is_open():
                w.on_mouse_release(x, y)

        # Alltid spela spel när pausmenyn är stängd
        if self.is_paused and self.main_menu.is_closed():
            self.play()

    def add_fish(self):
        pfish = PfishSprite(self.carrot_list)
        self.pfish_list.append(pfish)
        self.all_sprite_list.append(pfish)
    
    def enable_fps(self):
        self.show_fps = True

def main():
    print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
