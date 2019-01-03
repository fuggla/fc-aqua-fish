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
from classes.plant_blueberry import PlantBlueberry
from classes.plant_foreground import PlantForeground
from classes.fish_egg import FishEggSprite
from classes.window import Window
from classes.timer import Performance_timer
from classes.bubble_map import Bubble_map
from classes.fade import Fade
from classes.fps import Fps
from functions.diagnose_name_gender_health_hungry import diagnose_name_gender_health_hungry
from vars import *
from fish_vars import PFISH_NUMBER, BFISH_NUMBER, SHARK_NUMBER, pfish_egg_freq, bfish_egg_freq, shark_egg_freq


class MyGame(arcade.Window, State):

    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=FULLSCREEN)

        self.frame_count = 0
        self.show_windows = True
        self.background = None

        # If you have sprite lists, you should create them here

        self.sprite_list_names = [ "pfish", "bfish", "shark", "carrot", "plant_blueberry", "plant_foreground", "fish_egg", "all_sprite" ]
        for l in self.sprite_list_names:
            setattr(self, l + "_list", None)

        self.shape_list_names = [ "window", "bubble" ]
        for s in self.shape_list_names:
            setattr(self, l + "_list", None)

    def setup(self):
        if DEBUG:
            self.timer = Performance_timer("Setup started")

        # Skapa listor
        for l in self.sprite_list_names:
            setattr(self, l + "_list", arcade.SpriteList())
        self.window_list = self.create_windows()
        self.bubble_list = self.create_bubbles()

        """ Skapa alla fiskar """
        # Skapa purple_fish
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.carrot_list)
            self.pfish_list.append(pfish)
            self.all_sprite_list.append(pfish)

        # Skapa blue_small_fish
        for i in range(BFISH_NUMBER):
            bfish = BfishSprite(self.carrot_list, self.bfish_list, self.shark_list)
            self.bfish_list.append(bfish)
            self.all_sprite_list.append(bfish)

        # Skapa shark
        for i in range(SHARK_NUMBER):
            shark = SharkSprite(self.bfish_list, self.event)
            self.shark_list.append(shark)
            self.all_sprite_list.append(shark)

        # Skapa blåbärsväxter
        for i in range(PLANT_BLUEBERRY_NUMBER):
            plant_blueberry = PlantBlueberry(self.plant_blueberry_list)
            self.plant_blueberry_list.append(plant_blueberry)

        # Skapa förgrundsväxter
        for i in range(PLANT_FOREGROUND_NUMBER):
            plant_foreground = PlantForeground(self.plant_foreground_list)
            self.plant_foreground_list.append(plant_foreground)

        # Ladda backgrund
        self.background = arcade.load_texture(BACKGROUND_IMAGE)

        # Tona in grafik över ~2 sekunder
        self.fade = Fade(a=255, time=2)
        self.fade.start_in()

        # Räkna Frames Per Second
        self.fps_counter = Fps()

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
        self.fps_counter.draw()

    def update(self, delta_time):

        # Uppdatera all när spelet är igång
        if self.is_playing():
            self.plant_blueberry_list.update()
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
                    self.event.put(fish.get_name() + " laid an egg")

            for fish in self.bfish_list:
                # Ätalgoritm för blue small fish
                hit_list = arcade.check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1)        # 1 är hur mycket de äter varje tugga
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > SCREEN_HEIGHT and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är mätt
                if fish.health > fish.base_health * 1.1 and fish.name_gender[1] == "f" and random.randrange(1000) < bfish_egg_freq:
                    fish.health = fish.base_health
                    egg = FishEggSprite(fish, "small")
                    self.fish_egg_list.append(egg)
                    self.event.put(fish.get_name() + " laid an egg")

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
                    self.event.put(fish.get_name() + " laid an egg")

            """ Stega igenom äggen """
            for egg in self.fish_egg_list:
                if egg.age == egg.hatch_age:        # ägget kläcks efter en viss tid
                    egg.texture = egg.texture_egg_cracked
                    if egg.origin == "pfish":
                        # Kläck en pfish om ägget kom från pfish
                        fish = PfishSprite(self.carrot_list, setpos_x=egg.center_x, setpos_y=egg.center_y)
                        self.pfish_list.append(fish)
                    if egg.origin == "bfish":
                        # Kläck en bfish om ägget kom från bfish
                        fish = BfishSprite(self.carrot_list, self.bfish_list, self.shark_list, setpos_x=egg.center_x, setpos_y=egg.center_y)
                        self.bfish_list.append(fish)
                    if egg.origin == "shark":
                        # Kläck en shark om ägget kom från haj
                        fish = SharkSprite(self.bfish_list, setpos_x=egg.center_x, setpos_y=egg.center_y, event=self.event)
                        self.shark_list.append(fish)
                    self.all_sprite_list.append(fish)
                    self.event.put(fish.get_name() + " hatched!")
                if egg.age > egg.disapear_age:      # Ta bort äggresterna efter ett tag
                    egg.kill()
                egg.age += 1

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(delta_time)

            self.event.update()
            self.fade.update(delta_time)

        self.fps_counter.calculate(delta_time)
        self.frame_count += 1

    def on_key_release(self, key, key_modifiers):
        # Avsluta spel
        if (key == arcade.key.Q):
            arcade.window_commands.close_window()
        # Starta om
        elif (key == arcade.key.R):
            self.setup()
        # Visa pausemeny
        elif (key == arcade.key.ESCAPE):
            self.pause.toggle() # Fönster
            self.toggle_pause()  # State
        elif (key == arcade.key.F1):
            global DIAGNOSE_FISH
            if DIAGNOSE_FISH:
                DIAGNOSE_FISH = False
            else:
                DIAGNOSE_FISH = True
        elif (key == arcade.key.F2):
            self.fps_counter.toggle()
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
        if self.is_paused and self.pause.is_closed():
            self.play()

    def buy(self, thing):
        if (thing == "pfish"):
            color = ["purple", "orange", "green"]
            thing = PfishSprite(self.carrot_list, color=color[random.randrange(3)], setpos_y=SCREEN_HEIGHT, setspeed_y=-30)
            self.pfish_list.append(thing)
        elif (thing == "bfish"):
            thing = BfishSprite(self.carrot_list, self.bfish_list, self.shark_list, setpos_y=SCREEN_HEIGHT, setspeed_y=-30)
            self.bfish_list.append(thing)
            self.all_sprite_list.append(thing)
        elif (thing == "shark"):
            thing = SharkSprite(self.bfish_list, setpos_y=SCREEN_HEIGHT, setspeed_y=-30, event=self.event)
            self.shark_list.append(thing)
            self.all_sprite_list.append(thing)
        elif (thing == "carrot"):
            thing = CarrotSprite()
            self.carrot_list.append(thing)

        self.all_sprite_list.append(thing)
        self.event.put("Bought " + thing + " " + pfish.get_name())

    def buy_pfish(self):
        self.buy("pfish")

    def buy_bfish(self):
        self.buy("bfish")

    def buy_carrot(self):
        self.buy("carrot")

    def buy_shark(self):
        self.buy("shark")

    def create_windows(self):

        # Fönster för händelser
        event = Window(110, 60, 200, 100, " Events", title_height=20, title_align="left")
        self.event = event.add_text(15, 12, 180, 80)
        event.open()

        # Skapa meny för att interagera med akvariet
        action= Window(60, SCREEN_HEIGHT / 2, 100, 170, " Store", title_height=20, title_align="left")
        action.add_button(10, 10, 80, 30, "Pfish", 11, self.buy_pfish)
        action.add_button(50, 10, 80, 30, "Bfish", 11, self.buy_bfish)
        action.add_button(90, 10, 80, 30, "Shark", 11, self.buy_shark)
        action.add_button(130, 10, 80, 30, "Carrot", 11, self.buy_carrot)
        action.open()

        # Skapa huvudmeny att visa med escape
        pause=Window(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 130, "Aqua Fish")
        pause.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        pause.add_button(50, 10, 180, 30, "Open Store", 11, action.open)
        pause.add_button(90, 10, 180, 30, "Exit", 11, arcade.window_commands.close_window)
        self.pause = pause

        return [event, action, pause]

    def create_bubbles(self):
        list = []
        for i in range(BUBBLE_MAPS):
            list.append(Bubble_map())
        return list

def main():
    if DEBUG:
        print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
