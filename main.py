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
from classes.shark import SharkSprite
from classes.carrot import CarrotSprite
from classes.blueberry import BlueberrySprite
from classes.plant_blueberry import PlantBlueberry
from classes.plant_foreground import PlantForeground
from classes.fish_egg import FishEggSprite
from classes.window import Window
from classes.timer import Performance_timer
from classes.bubble_map import Bubble_map
from classes.fade import Fade
from functions.diagnose_name_gender_health_hungry import diagnose_name_gender_health_hungry
from vars import *
from fish_vars import PFISH_NUMBER, BFISH_NUMBER, SHARK_NUMBER, pfish_egg_freq, bfish_egg_freq, shark_egg_freq


class MyGame(arcade.Window, State):

    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=FULLSCREEN)

        self.frame_count = 0
        self.show_windows = True

        # If you have sprite lists, you should create them here
        self.pfish_list = None
        self.bfish_list = None
        self.shark_list = None
        self.carrot_list = None
        self.blueberry_list = None
        self.blueberry_list = None
        self.plant_blueberry_list = None
        self.plant_foreground_list = None
        self.fish_egg_list = None
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

        # Skapa fönster
        self.window_list = []

        # Fönster för händelser
        self.event_window = Window(110, 60, 200, 100, " Events", title_height=20, title_align="left")
        self.event = self.event_window.add_text(15, 12, 180, 80)
        self.window_list.append(self.event_window)
        self.event_window.open()

        # Skapa meny för att interagera med akvariet
        self.interaction_window = Window(60, SCREEN_HEIGHT / 2, 100, 170, " Store", title_height=20, title_align="left")
        self.interaction_window.add_button(10, 10, 80, 30, "Pfish", 11, self.buy_pfish)
        self.interaction_window.add_button(50, 10, 80, 30, "Bfish", 11, self.buy_bfish)
        self.interaction_window.add_button(90, 10, 80, 30, "Shark", 11, self.buy_shark)
        self.interaction_window.add_button(130, 10, 80, 30, "Carrot", 11, self.buy_carrot)
        self.window_list.append(self.interaction_window)
        self.interaction_window.open()

        # Skapa huvudmeny att visa med escape
        self.main_menu_window = Window(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 130, "Aqua Fish")
        self.main_menu_window.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        self.main_menu_window.add_button(50, 10, 180, 30, "Open Store", 11, self.interaction_window.open)
        self.main_menu_window.add_button(90, 10, 180, 30, "Exit", 11, arcade.window_commands.close_window)
        self.window_list.append(self.main_menu_window)
        if DEBUG:
            self.timer.print("Created windows")

        # Alla arcade sprites och sprites_list här
        self.pfish_list = arcade.SpriteList()
        self.bfish_list = arcade.SpriteList()
        self.shark_list = arcade.SpriteList()
        self.carrot_list = arcade.SpriteList()
        self.blueberry_list = arcade.SpriteList()
        self.plant_blueberry_list = arcade.SpriteList()
        self.plant_foreground_list = arcade.SpriteList()
        self.fish_egg_list = arcade.SpriteList()
        self.all_sprite_list = arcade.SpriteList()

        """ Skapa alla fiskar """
        # Skapa purple_fish
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.carrot_list)
            self.pfish_list.append(pfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(pfish)                      # och i totallistan
        if DEBUG:
            self.timer.print("Created purple_fish")

        # Skapa blue_small_fish
        for i in range(BFISH_NUMBER):
            bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list)
            self.bfish_list.append(bfish)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(bfish)                      # och i totallistan
        if DEBUG:
            self.timer.print("Created blue_small fish")

        # Skapa shark
        for i in range(SHARK_NUMBER):
            shark = SharkSprite(self.bfish_list, self.event)
            self.shark_list.append(shark)                           # Lägg till fiskarna i fisklistan
            self.all_sprite_list.append(shark)                      # och i totallistan
        if DEBUG:
            self.timer.print("Created shark")

        # Skapa blåbärsväxter
        for i in range(PLANT_BLUEBERRY_NUMBER):
            plant_blueberry = PlantBlueberry(self.plant_blueberry_list)
            self.plant_blueberry_list.append(plant_blueberry)

        # Skapa förgrundsväxter
        for i in range(PLANT_FOREGROUND_NUMBER):
            plant_foreground = PlantForeground(self.plant_foreground_list)
            self.plant_foreground_list.append(plant_foreground)

        # Skapa bubblor
        self.bubble_list = []
        for i in range(BUBBLE_MAPS):
            self.bubble_list.append(Bubble_map())
        if DEBUG:
            self.timer.print("Created bubbles")

        # Ladda backgrund
        self.background = arcade.load_texture(BACKGROUND_IMAGE)

        # Tona in grafik över ~2 sekunder
        self.fade = Fade(a=255, time=2)
        self.fade.start_in()

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

        self.plant_blueberry_list.draw()
        self.blueberry_list.draw()
        self.fish_egg_list.draw()
        self.all_sprite_list.draw()
        self.plant_foreground_list.draw()

        # "DIAGNOSE_FISH = True" skriver ut health och hungry för varje fisk. (För balans av mat och hunger)
        if DIAGNOSE_FISH:
            diagnose_name_gender_health_hungry(self.pfish_list)
            diagnose_name_gender_health_hungry(self.bfish_list)
            diagnose_name_gender_health_hungry(self.shark_list)

        if self.show_windows:
            for w in self.window_list:
                w.draw()

        self.fade.draw()

        # Rita FPS uppe i högra hörnet
        if self.show_fps:
            arcade.draw_text(str(self.fps), 10, SCREEN_HEIGHT - 10, arcade.color.BLACK, font_size=8, width=10, align="left", anchor_x="center", anchor_y="center")

    def update(self, delta_time):

        # Uppdatera all när spelet är igång
        if self.is_playing():
            self.plant_blueberry_list.update()
            self.blueberry_list.update()
            self.fish_egg_list.update()
            self.all_sprite_list.update()
            self.plant_foreground_list.update()

            """ Skapa en morot med sannolikheten 1 på 1000 varje frame """
            if random.randrange(500) < 1:
                carrot = CarrotSprite()
                self.carrot_list.append(carrot)
                self.all_sprite_list.append(carrot)

            """ Här stegas alla fiskar igenom för mat, död och ägg mm """

            for fish in self.pfish_list:
                # Ätalgoritm för purple fish
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 10)       # 10 är hur mycket de äter varje tugga
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > SCREEN_HEIGHT and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är mätt
                if fish.health > fish.base_health * 1.1 and fish.name_gender[1] == "f" and random.randrange(1000) < pfish_egg_freq:
                    fish.health = fish.base_health
                    egg = FishEggSprite(fish, "medium")
                    self.fish_egg_list.append(egg)

            for fish in self.bfish_list:
                # Ätalgoritm för blue small fish
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1)        # 1 är hur mycket de äter varje tugga

                # Ätalgoritm för blue small fish
                hit_list = arcade.check_for_collision_with_list(fish, self.blueberry_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1)  # 1 är hur mycket de äter varje tugga

                # Ta bort döda fiskar som flytit upp
                if fish.bottom > SCREEN_HEIGHT and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är mätt
                if fish.health > fish.base_health * 1.1 and fish.name_gender[1] == "f" and random.randrange(1000) < bfish_egg_freq:
                    fish.health = fish.base_health
                    egg = FishEggSprite(fish, "small")
                    self.fish_egg_list.append(egg)

            for fish in self.shark_list:
                # Ätalgoritm för blue shark
                if fish.iseating > 0:
                    fish.iseating -= 1
                hit_list = arcade.check_for_collision_with_list(fish, self.bfish_list)
                # Om fisken lever och det finns en blue small fish äter fisken den
                if hit_list and fish.isalive:
                    fish.eat_fish(hit_list[0])
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > SCREEN_HEIGHT and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är mätt
                if fish.health > fish.base_health * 1.1 and fish.name_gender[1] == "f" and random.randrange(1000) < shark_egg_freq:
                    fish.health = fish.base_health
                    egg = FishEggSprite(fish, "large")
                    self.fish_egg_list.append(egg)


            """ Stega igenom äggen """
            for egg in self.fish_egg_list:
                if egg.age == egg.hatch_age:        # ägget kläcks efter en viss tid
                    egg.texture = egg.texture_egg_cracked
                    if egg.origin == "pfish":
                        # Kläck en pfish om ägget kom från pfish
                        pfish = PfishSprite(self.carrot_list, setpos_x=egg.center_x, setpos_y=egg.center_y)
                        self.pfish_list.append(pfish)
                        self.all_sprite_list.append(pfish)
                    if egg.origin == "bfish":
                        # Kläck en bfish om ägget kom från bfish
                        bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list, setpos_x=egg.center_x, setpos_y=egg.center_y)
                        self.bfish_list.append(bfish)
                        self.all_sprite_list.append(bfish)
                    if egg.origin == "shark":
                        # Kläck en shark om ägget kom från haj
                        shark = SharkSprite(self.bfish_list, setpos_x=egg.center_x, setpos_y=egg.center_y, event=self.event)
                        self.shark_list.append(shark)
                        self.all_sprite_list.append(shark)
                if egg.age > egg.disapear_age:      # Ta bort äggresterna efter ett tag
                    egg.kill()
                egg.age += 1

            for plant in self.plant_blueberry_list:
                if random.randrange(1000) < plant_blueberry_grow_rate:
                    berry = BlueberrySprite(plant.center_x, plant.center_y)
                    self.blueberry_list.append(berry)

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(delta_time)

            self.event.update()
            self.fade.update(delta_time)

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
            self.main_menu_window.toggle()
            self.toggle_pause()
        elif (key == arcade.key.F1):
            global DIAGNOSE_FISH
            if DIAGNOSE_FISH:
                DIAGNOSE_FISH = False
            else:
                DIAGNOSE_FISH = True
        elif (key == arcade.key.F2):
            self.show_fps = not self.show_fps
        elif (key == arcade.key.F3):
            self.fade.start()
        elif (key == arcade.key.SPACE):
            self.show_windows = not self.show_windows

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        # Fönster som är i läge "dragged" följer musens kordinater
        if self.show_windows:
            for w in self.window_list:
                if w.is_dragged():
                    w.move(delta_x, delta_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Fönster kan triggas av att muspekaren klickas ovanför en knapp
        if self.show_windows:
            for w in self.window_list:
                if w.is_open():
                    w.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Fönster kan triggas av att muspekaren släpps ovan för en knapp
        if self.show_windows:
            for w in self.window_list:
                if w.is_open():
                    w.on_mouse_release(x, y)

        # Alltid spela spel när pausmenyn är stängs
        if self.is_paused and self.main_menu_window.is_closed():
            self.play()

    def buy_pfish(self):
        color = ["purple", "orange", "green"]
        pfish = PfishSprite(self.carrot_list, color=color[random.randrange(3)], setpos_y=SCREEN_HEIGHT, setspeed_y=-30)
        self.pfish_list.append(pfish)
        self.all_sprite_list.append(pfish)
        self.event.put("Bought pfish " + pfish.get_name())

    def buy_bfish(self):
        bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list, setpos_y=SCREEN_HEIGHT, setspeed_y=-30)
        self.bfish_list.append(bfish)
        self.all_sprite_list.append(bfish)
        self.event.put("Bought bfish" + bfish.get_name())

    def buy_carrot(self):
        carrot = CarrotSprite()
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)
        self.event.put("Bought carrot")

    def buy_shark(self):
        shark = SharkSprite(self.bfish_list, setpos_y=SCREEN_HEIGHT, setspeed_y=-30, event=self.event)
        self.shark_list.append(shark)
        self.all_sprite_list.append(shark)
        self.event.put("Bought shark " + shark.get_name())

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
