"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types
from classes.state import State
from classes.button import Button
from classes.purple_fish import PfishSprite
from classes.blue_small_fish import BfishSprite
from classes.carrot import CarrotSprite
from classes.window import Window
from classes.timer import Performance_timer
from classes.bubble_map import Bubble_map
from functions.diagnose_name_gender_health_hungry import diagnose_name_gender_health_hungry
from vars import *
from fish_vars import PFISH_NUMBER, BFISH_NUMBER

class MyGame(arcade.Window, State):

    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=FULLSCREEN)

        self.frame_count = 0

        # If you have sprite lists, you should create them here
        self.pfish_list = None
        self.bfish_list = None
        self.carrot_list = None
        self.all_sprite_list = None
        self.window_list = None
        self.background = None
        self.bubble_list = None

        # FPS
        self.fps = 0
        self.tick = 0
        self.delta_count = 0
        self.show_fps = False

    def setup(self):
        if DEBUG:
            self.timer = Performance_timer("Setup started")

        # Alla arcade sprites och sprites_list här
        self.pfish_list = arcade.SpriteList()
        self.bfish_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        # Skapa purple_fish
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.carrot_list)
            self.pfish_list.append(pfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(pfish)                      # och i totallistan
        if DEBUG:
            self.timer.print("Created purple_fish")

        # Skapa blue_small_fish
        for i in range(BFISH_NUMBER):
            bfish = BfishSprite(self.carrot_list, self.bfish_list)
            self.bfish_list.append(bfish)  # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(bfish)  # och i totallistan
        if DEBUG:
            self.timer.print("Created blue_small fish")

        # Skapa fönster
        self.window_list = []

        # Skapa meny för att interagera med akvariet
        self.interaction_menu = Window(60, SCREEN_HEIGHT / 2, 100, 130, " Store", title_height=20, title_align="left")
        self.interaction_menu.add_button(10, 10, 80, 30, "Pfish", 11, self.buy_pfish)
        self.interaction_menu.add_button(50, 10, 80, 30, "Bfish", 11, self.buy_bfish)
        self.interaction_menu.add_button(90, 10, 80, 30, "Carrot", 11, self.buy_carrot)
        self.window_list.append(self.interaction_menu)
        self.interaction_menu.open()

        # Skapa huvudmeny att visa med escape
        self.main_menu = Window(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 130, "Aqua Fish")
        self.main_menu.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        self.main_menu.add_button(50, 10, 180, 30, "Open Store", 11, self.interaction_menu.open)
        self.main_menu.add_button(90, 10, 180, 30, "Exit", 11, arcade.window_commands.close_window)
        self.window_list.append(self.main_menu)
        if DEBUG:
            self.timer.print("Created windows")

        # Skapa bubblor
        self.bubble_list = []
        for i in range(BUBBLE_MAPS):
            self.bubble_list.append(Bubble_map())
        if DEBUG:
            self.timer.print("Created bubbles")

        # Ladda backgrund
        self.background = arcade.load_texture(BACKGROUND_IMAGE)

        # Setup klar, starta spelet
        if DEBUG:
            self.timer.done("Setup done")
        self.play()

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Rita bakgrund
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        for b in self.bubble_list:
            b.draw()

        self.all_sprite_list.draw()

        # "DIAGNOSE_FISH = True" skriver ut health och hungry för varje fisk. (För balans av mat och hunger)
        if DIAGNOSE_FISH:
            diagnose_name_gender_health_hungry(self.pfish_list)
            diagnose_name_gender_health_hungry(self.bfish_list)

        for w in self.window_list:
            w.draw()

        # Rita FPS uppe i högra hörnet
        if self.show_fps:
            arcade.draw_text(str(self.fps), 10, SCREEN_HEIGHT - 10, arcade.color.BLACK, font_size=8, width=10, align="left", anchor_x="center", anchor_y="center")

    def update(self, delta_time):

        # Uppdatera all när spelet är igång
        if self.is_playing():
            self.all_sprite_list.update()

            """ Skapa en morot med sannolikheten 1 på 1000 varje frame """
            if random.randrange(500) < 1:
                carrot = CarrotSprite()
                self.carrot_list.append(carrot)
                self.all_sprite_list.append(carrot)

            """ Ätalgoritmerna för fiskarna """
            # Ätalgoritm för purple fish
            for fish in self.pfish_list:
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 10)       # 10 är hur mycket de äter varje tugga
                if fish.bottom > SCREEN_HEIGHT:
                    fish.kill()

            # Ätalgoritm för blue small fish
            for fish in self.bfish_list:
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1)        # 1 är hur mycket de äter varje tugga
                if fish.bottom > SCREEN_HEIGHT:
                    fish.kill()

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(delta_time)

        # Räkna ut FPS en gång per sekund
        if self.show_fps:
            self.tick += 1
            self.delta_count += delta_time
            if self.delta_count >= 1:
                self.fps = self.tick
                self.delta_count = 0
                self.tick = 0

        self.frame_count += 1

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        # Avsluta spel
        if (key == arcade.key.Q):
            arcade.window_commands.close_window()
        # Starta om
        elif (key == arcade.key.R):
            self.setup()
        # Visa pausemeny
        elif (key == arcade.key.ESCAPE):
            self.main_menu.toggle()
            self.toggle_pause()
        elif (key == arcade.key.F1):
            global DIAGNOSE
            DIAGNOSE = not DIAGNOSE
        elif (key == arcade.key.F2):
            self.show_fps = not self.show_fps

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        # Fönster som är i läge "dragged" följer musens kordinater
        for w in self.window_list:
            if w.is_dragged():
                w.move(delta_x, delta_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Fönster kan triggas av att muspekaren klickas ovanför en knapp
        for w in self.window_list:
            if w.is_open():
                w.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Fönster kan triggas av att muspekaren släpps ovan för en knapp
        for w in self.window_list:
            if w.is_open():
                w.on_mouse_release(x, y)

        # Alltid spela spel när pausmenyn är stängs
        if self.is_paused and self.main_menu.is_closed():
            self.play()

    def buy_pfish(self):
        color = ["purple", "orange", "green"]
        pfish = PfishSprite(self.carrot_list, color=color[random.randrange(3)])
        self.pfish_list.append(pfish)
        self.all_sprite_list.append(pfish)

    def buy_bfish(self):
        bfish = BfishSprite(self.carrot_list, self.bfish_list)
        self.bfish_list.append(bfish)
        self.all_sprite_list.append(bfish)

    def buy_carrot(self):
        carrot = CarrotSprite()
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)

    # Visa FPS längst upp till vänster
    def enable_fps(self):
        self.show_fps = True

def main():
    if DEBUG:
        print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
