"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types
from arcade import SpriteList, load_texture, start_render, draw_texture_rectangle, check_for_collision_with_list, window_commands
from arcade.key import *
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
        self.center_cords = (width // 2, height // 2)
        self.width_height = (width, height)

        # Sätt spritelistor och vanliga listor till none
        self.sprite_list_names = [ "pfish", "bfish", "shark", "carrot", "blueberry", "plant_blueberry", "plant_foreground", "fish_egg", "all_sprite" ]
        self.standard_list_names = [ "window", "bubble", "berry_info" ]
        for l in self.sprite_list_names + self.standard_list_names:
            setattr(self, f"{l}_list", None)

    def setup(self):
        if DEBUG:
            self.timer = Performance_timer("Setup started")

        # Skapa listor
        for l in self.sprite_list_names:
            setattr(self, f"{l}_list", SpriteList())
        self.berry_info_list = []
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
            bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list)
            self.bfish_list.append(bfish)
            self.all_sprite_list.append(bfish)

        # Skapa shark
        for i in range(SHARK_NUMBER):
            shark = SharkSprite(self.bfish_list, self.event)
            self.shark_list.append(shark)
            self.all_sprite_list.append(shark)

        # Skapa blåbärsväxter
        for i in range(PLANT_BLUEBERRY_NUMBER):
            plant_blueberry = PlantBlueberry(self.plant_blueberry_list, i)
            self.plant_blueberry_list.append(plant_blueberry)
            self.berry_info_list.append(plant_blueberry.berry_info)

        # Skapa förgrundsväxter
        for i in range(PLANT_FOREGROUND_NUMBER):
            plant_foreground = PlantForeground(self.plant_foreground_list)
            self.plant_foreground_list.append(plant_foreground)

        # Ladda backgrund
        self.background = load_texture(BACKGROUND_IMAGE)

        # Tona in grafik över ~2 sekunder
        self.fade = Fade(a=255, time=2)
        self.fade.start_in()

        # Räkna Frames Per Second
        self.fps_counter = Fps()

        # Setup klar, starta spelet
        if DEBUG:
            self.timer = self.timer.done("Setup done")
        self.play()

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()

        # Rita bakgrund
        draw_texture_rectangle(*self.center_cords, *self.width_height, self.background)

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
        self.fps_counter.draw()

    def update(self, dt):

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
                hit_list = check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 10)       # 10 är hur mycket de äter varje tugga
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är mätt
                if fish.health > fish.base_health * 1.1 and fish.name_gender[1] == "f" and random.randrange(1000) < pfish_egg_freq:
                    fish.health = fish.base_health
                    egg = FishEggSprite(fish, "medium")
                    self.fish_egg_list.append(egg)

            for fish in self.bfish_list:
                # Ätalgoritm för blue small fish
                hit_list = check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1)        # 1 är hur mycket de äter varje tugga

                # Ätalgoritm för blue small fish
                hit_list = check_for_collision_with_list(fish, self.blueberry_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and fish.isalive:
                    fish.eat_food(hit_list[0], 1, berry_info_list=self.berry_info_list)  # 1 är hur mycket de äter varje tugga

                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
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
                hit_list = check_for_collision_with_list(fish, self.bfish_list)
                # Om fisken lever och det finns en blue small fish äter fisken den
                if hit_list and fish.isalive:
                    fish.eat_fish(hit_list[0])
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
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

            """ Stega igenom blåbärsplantorna """
            for i in range(len(self.berry_info_list)):
                for k in range(2):
                    if random.randrange(1000) < plant_blueberry_grow_rate and not self.berry_info_list[i][2 + k]:
                        berry = BlueberrySprite(self.berry_info_list[i][k][0], self.berry_info_list[i][k][1], self.berry_info_list[i][4], k)
                        self.berry_info_list[i][2 + k] = True
                        self.blueberry_list.append(berry)

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(dt)

            self.event.update()
            self.fade.update(dt)

        self.fps_counter.calculate(dt)
        self.frame_count += 1

    def on_key_release(self, key, key_modifiers):
        # Avsluta spel
        if (key == Q):
            window_commands.close_window()
        # Starta om
        elif (key == R):
            self.setup()
        # Visa pausemeny
        elif (key == ESCAPE):
            self.pause.toggle() # Fönster
            self.toggle_pause()  # State
        elif (key == F1):
            global DIAGNOSE_FISH
            DIAGNOSE_FISH = not DIAGNOSE_FISH
        elif (key == F2):
            self.fps_counter.toggle()
        elif (key == F3):
            self.fade.start()
        elif (key == SPACE):
            self.show_windows = not self.show_windows

    def on_mouse_motion(self, x, y, dx, dy):
        # Fönster som är i läge "dragged" följer musens kordinater
        if self.show_windows:
            for w in self.window_list:
                if w.is_dragged():
                    w.move(dx, dy)

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

    def buy_fish(self, name):
        fish = None
        if (name == "pfish"):
            color = ["purple", "orange", "green"]
            fish = PfishSprite(self.carrot_list, color=color[random.randrange(3)], setpos_y=self.height, setspeed_y=-30)
            self.pfish_list.append(fish)
        elif (name == "bfish"):
            fish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list, setpos_y=self.height, setspeed_y=-30)
            self.bfish_list.append(fish)
        elif (name == "shark"):
            fish = SharkSprite(self.bfish_list, setpos_y = self.height, setspeed_y=-30, event=self.event)
            self.shark_list.append(fish)

        # Done and done
        self.all_sprite_list.append(fish)
        self.event.put(f"Bought {name} {fish.get_name()}")

    def buy_shark(self):
        self.buy_fish("shark")

    def buy_pfish(self):
        self.buy_fish("pfish")

    def buy_bfish(self):
        self.buy_fish("bfish")

    def buy_carrot(self):
        carrot = CarrotSprite()
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)
        self.event.put("Bought carrot")

    def create_windows(self):
        # Fönster för händelser
        event = Window(110, 60, 200, 100, " Events", title_height=20, title_align="left")
        self.event = event.add_text(15, 12, 180, 80) # använd self.event.put(text) för nya rader
        event.open()

        # Skapa meny för att interagera med akvariet
        action= Window(60, self.height/ 2, 100, 170, " Store", title_height=20, title_align="left")
        action.add_button(10, 10, 80, 30, "Pfish", 11, self.buy_pfish)
        action.add_button(50, 10, 80, 30, "Bfish", 11, self.buy_bfish)
        action.add_button(90, 10, 80, 30, "Shark", 11, self.buy_shark)
        action.add_button(130, 10, 80, 30, "Carrot", 11, self.buy_carrot)
        action.open()

        # Skapa huvudmeny att visa med escape
        pause=Window(*self.center_cords, 200, 130, "Aqua Fish")
        pause.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        pause.add_button(50, 10, 180, 30, "Open Store", 11, action.open)
        pause.add_button(90, 10, 180, 30, "Exit", 11, window_commands.close_window)
        self.pause = pause # Behövs för att bland annat escape ska fungera

        return [event, action, pause]

    def create_bubbles(self):
        list = []
        for i in range(BUBBLE_MAPS):
            list.append(Bubble_map())
        return list

def main():
    if DEBUG:
        print(f"Starting Aqua Fish v{VERSION}")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
