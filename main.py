"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types, math
from arcade import SpriteList, load_texture, start_render, draw_texture_rectangle, check_for_collision_with_list, window_commands, draw_rectangle_filled
from random import randrange
from arcade.key import *
from arcade.color import *
from classes.state import State
from classes.purple_fish import PfishSprite
from classes.blue_small_fish import BfishSprite
from classes.shark import SharkSprite
from classes.carrot import CarrotSprite
from classes.blueberry import BlueberrySprite
from classes.plant_blueberry import PlantBlueberry
from classes.plant_foreground import PlantForeground
from classes.fish_egg import FishEggSprite
from classes.window import Window, Button, Text
from classes.timer import Performance_timer
from classes.bubble_map import Bubble_map
from classes.fade import Fade
from classes.fps import Fps
from classes.pointer import Pointer
from functions.diagnose_name_gender_health_hungry import diagnose_name_gender_health_hungry
from vars import *
from fish_vars import PFISH_NUMBER, BFISH_NUMBER, SHARK_NUMBER, pfish_size, bfish_size, shark_size


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
        self.standard_list_names = [ "window", "bubble", "bubble_main", "berry_info"]
        for l in self.sprite_list_names + self.standard_list_names:
            setattr(self, f"{l}_list", None)

        self.set_mouse_visible(False)
        self.dragged_sprite = []

    def setup(self):
        self.timer = Performance_timer("Loading started")

        # Skapa listor
        for l in self.sprite_list_names:
            setattr(self, f"{l}_list", SpriteList())
        self.berry_info_list = []
        self.window_list = self.create_windows()
        self.bubble_list = self.create_bubbles()
        self.bubble_main_list = self.create_bubbles((0,0,0,randrange(64,192)))
        self.pointer = SpriteList()
        self.pointer.use_spatial_hash = False

        """ Skapa alla fiskar """
        # Skapa purple_fish
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.carrot_list, self.pfish_list)
            self.pfish_list.append(pfish)
            self.all_sprite_list.append(pfish)

        # Skapa blue_small_fish
        for i in range(BFISH_NUMBER):
            bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list)
            self.bfish_list.append(bfish)
            self.all_sprite_list.append(bfish)

        # Skapa shark
        for i in range(SHARK_NUMBER):
            shark = SharkSprite(self.bfish_list, self.shark_list, self.event)
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

        # Räkna Frames Per Second
        self.fps_counter = Fps()

        # Skapa muspekaren
        self.pointer.append(Pointer())

        # Setup klar. Använd timer för att vänta med toning
        # Tona in grafik över ~2 sekunder
        self.fade = Fade(a=255, time=2, pause=self.timer.done("Loading done"))
        self.fade.start_in()

        if SKIP_MAIN_MENU:
            self.start()
        else:
            self.state_main_menu()

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()

        if self.is_playing():
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

        elif self.is_main_menu():
            self.window_list[0].draw()
            for b in self.bubble_main_list:
                b.draw()

        self.fade.draw()

        # Rita FPS uppe i högra hörnet
        self.fps_counter.draw()

        # Rita ut muspekaren
        self.pointer.draw()

    def update(self, dt):

        # Uppdatera all när spelet är igång
        if self.is_playing():
            self.plant_blueberry_list.update()
            self.blueberry_list.update()
            self.fish_egg_list.update()
            self.all_sprite_list.update()
            self.plant_foreground_list.update()

            """ Skapa en morot med sannolikheten 1 på 1000 varje frame """
            if random.randrange(1000) < carrot_frequency:
                carrot = CarrotSprite(setspeed_y=-20)
                self.carrot_list.append(carrot)
                self.all_sprite_list.append(carrot)

            """ Här stegas alla fiskar igenom för mat, död och ägg mm """
            for fish in self.pfish_list:
                # Ätalgoritm för purple fish
                hit_list = check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and not fish.disturbed:
                    fish.eat_food(hit_list[0], 10)       # 10 är hur mycket de äter varje tugga
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är gravid
                if fish.ready_to_lay_egg:
                    fish.pregnant = False
                    fish.ready_to_lay_egg = False
                    fish.laid_eggs += 1
                    egg = FishEggSprite(fish, "medium")
                    self.fish_egg_list.append(egg)

            for fish in self.bfish_list:
                # Ätalgoritm för blue small fish
                hit_list = check_for_collision_with_list(fish, self.carrot_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and not fish.disturbed:
                    fish.eat_food(hit_list[0], 1)        # 1 är hur mycket de äter varje tugga

                # Ätalgoritm för blue small fish
                hit_list = check_for_collision_with_list(fish, self.blueberry_list)
                if len(hit_list) == 0 and fish.iseating > 0:
                    fish.iseating -= 1
                # Om fisken lever och det finns en morot äter fisken på den
                if hit_list and not fish.disturbed:
                    fish.eat_food(hit_list[0], 1)  # 1 är hur mycket de äter varje tugga

                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är gravid
                if fish.ready_to_lay_egg:
                    fish.pregnant = False
                    fish.ready_to_lay_egg = False
                    fish.laid_eggs += 1
                    egg = FishEggSprite(fish, "small")
                    self.fish_egg_list.append(egg)

            for fish in self.shark_list:
                # Ätalgoritm för blue shark
                if fish.iseating > 0:
                    fish.iseating -= 1
                hit_list = check_for_collision_with_list(fish, self.bfish_list)
                # Om fisken lever och det finns en blue small fish äter fisken den
                if hit_list and not fish.disturbed:
                    fish.eat_fish(hit_list[0])
                # Ta bort döda fiskar som flytit upp
                if fish.bottom > self.height and fish.health <= 0:
                    fish.kill()
                # Lägg ägg ifall fisken är gravid
                if fish.ready_to_lay_egg:
                    fish.pregnant = False
                    fish.ready_to_lay_egg = False
                    fish.laid_eggs += 1
                    egg = FishEggSprite(fish, "large")
                    self.fish_egg_list.append(egg)

            """ Stega igenom äggen """
            for egg in self.fish_egg_list:
                if egg.age == egg.hatch_age:        # ägget kläcks efter en viss tid
                    egg.texture = egg.texture_egg_cracked
                    if egg.origin == "pfish":
                        # Kläck en pfish om ägget kom från pfish
                        pfish = PfishSprite(self.carrot_list, self.pfish_list, setpos_x=egg.center_x,
                                            setpos_y=egg.center_y, size=pfish_size*0.5)
                        self.pfish_list.append(pfish)
                        self.all_sprite_list.append(pfish)
                    if egg.origin == "bfish":
                        # Kläck en bfish om ägget kom från bfish
                        bfish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list, setpos_x=egg.center_x,
                                            setpos_y=egg.center_y, size=pfish_size*0.25)
                        self.bfish_list.append(bfish)
                        self.all_sprite_list.append(bfish)
                    if egg.origin == "shark":
                        # Kläck en shark om ägget kom från haj
                        shark = SharkSprite(self.bfish_list, self.shark_list, setpos_x=egg.center_x,
                                            setpos_y=egg.center_y, event=self.event, size=pfish_size*0.6)
                        self.shark_list.append(shark)
                        self.all_sprite_list.append(shark)
                if egg.age > egg.disapear_age:      # Ta bort äggresterna efter ett tag
                    egg.kill()
                egg.age += 1

            """ Stega igenom blåbärsplantorna """
            for grow_space in self.berry_info_list:
                for k in range(2):
                    if random.randrange(1000) < plant_blueberry_grow_rate:
                        test_x = grow_space[k][0]
                        test_y = grow_space[k][1]
                        can_grow = True
                        for test_berry in self.blueberry_list:
                            if math.fabs(test_berry.center_x - test_x) < 25:
                                can_grow = False
                        if can_grow:
                            berry = BlueberrySprite(test_x, test_y)
                            self.blueberry_list.append(berry)

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(dt)

            self.event.update()

        elif self.is_main_menu():
            for b in self.bubble_main_list:
                b.update(dt)

        self.fade.update(dt)
        self.fps_counter.calculate(dt)
        self.frame_count += 1

    def on_key_release(self, key, key_modifiers):
        if (key == Q): # Avsluta
            window_commands.close_window()
        elif (key == R): # Starta om
            self.setup()
        elif self.is_main_menu():
            return
        elif (key == ESCAPE): # Visa pausmeny och pausa
            self.pause.toggle()
            self.toggle_pause()
        elif (key == F1): # Info om fiskar
            global DIAGNOSE_FISH
            DIAGNOSE_FISH = not DIAGNOSE_FISH
        elif (key == F2): # Visa FPS
            self.fps_counter.toggle()
        elif (key == SPACE): # Visa fönster
            self.show_windows = not self.show_windows

    def on_mouse_motion(self, x, y, dx, dy):
        for w in self.get_open_windows(dragged_only=True):
            w.move(dx, dy)
        if self.dragged_sprite:                                         # Om det finns dragna sprites
            self.dragged_sprite[0].drag_sprite(x, y, dx, dy)            # Så flytta dem och spara pekarens hastighet

        # Här flyttas muspekaren då musen flyttas.
        # Allt jox är för att fingret ska hamna på samma plats som orginalmusens "pekare"
        self.pointer[0].set_position(x + self.pointer[0].width*0.3, y - self.pointer[0].height*0.5)

    def on_mouse_press(self, x, y, button, key_modifiers):
        for w in self.get_open_windows():
            w.on_mouse_press(x, y)
            if w.dragging:
                self.pointer[0].texture = self.pointer[0].texture_grab  # Om musen håller i ett fönster så byt textur
        for sprite in self.all_sprite_list:                             # Stega igenom alla fiskar och morötter
            if sprite.is_mouse_on(self.pointer[0]):                     # Kolla ifall de är i kontakt med pekaren
                self.dragged_sprite.append(sprite)                      # Spara dem i en lista
                self.pointer[0].texture = self.pointer[0].texture_grab  # Om musen håller i en fisk så byt textur

    def on_mouse_release(self, x, y, button, key_modifiers):
        for w in self.get_open_windows():
            w.on_mouse_release(x, y)
        if self.dragged_sprite:
            self.dragged_sprite[0].change_x = self.dragged_sprite[0].drag_speed[0]  # Ställ in spritens x-hastighet
            self.dragged_sprite[0].change_y = self.dragged_sprite[0].drag_speed[1]  # Ställ in spritens y-hastighet
            self.dragged_sprite = []                                                # Töm listan med dragna strukturer
        self.pointer[0].texture = self.pointer[0].texture_point                     # Byt tillbaka till vanliga texturen

        # Alltid spela spel när pausmenyn är stängs
        if self.is_paused() and self.pause.is_closed():
            self.play()

    # Hämta alla tillgängliga fönster
    def get_open_windows(self, dragged_only=False):
        open_windows = []
        if self.show_windows:
            for w in self.window_list:
                if w.is_dragged():
                    return [ w ]
                elif w.is_open() and not dragged_only:
                    open_windows.append(w)
        return open_windows

    def buy_fish(self, name):
        fish = None
        if (name == "pfish"):
            color = ["purple", "orange", "green"]
            fish = PfishSprite(self.carrot_list, self.pfish_list, color=color[random.randrange(3)], setpos_y=self.height, setspeed_y=-30)
            self.pfish_list.append(fish)
        elif (name == "bfish"):
            fish = BfishSprite(self.carrot_list, self.blueberry_list, self.bfish_list, self.shark_list, setpos_y=self.height, setspeed_y=-30)
            self.bfish_list.append(fish)
        elif (name == "shark"):
            fish = SharkSprite(self.bfish_list, self.shark_list, setpos_y = self.height, setspeed_y=-30, event=self.event)
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
        carrot = CarrotSprite(setspeed_y=-20)
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)
        self.event.put("Bought carrot")

    def create_windows(self):
        # Huvudmeny
        main = Window(*self.center_cords, *self.width_height, "Main Menu",
        background_color=WHITE)
        main.add_button(self.height / 2 - 30, self.width / 2 - 90, 180, 30, "New Game", 22, self.start, WHITE,
        WHITE, "Lato Light", GRAY)
        main.add_button(self.height / 2 + 30, self.width / 2 - 90, 180, 30, "Exit", 22,
        window_commands.close_window, WHITE, WHITE, "Lato Light", GRAY)
        main.open()

        # Fönster för händelser
        event = Window(110, 60, 200, 100, " Events", title_height=20, title_align="left")
        self.event = event.add_text(15, 12, 180, 80) # använd self.event.put(text) för nya rader

        # Skapa meny för att interagera med akvariet
        action= Window(60, self.height/ 2, 100, 170, " Store", title_height=20, title_align="left")
        action.add_button(10, 10, 80, 30, "Pfish", 11, self.buy_pfish)
        action.add_button(50, 10, 80, 30, "Bfish", 11, self.buy_bfish)
        action.add_button(90, 10, 80, 30, "Shark", 11, self.buy_shark)
        action.add_button(130, 10, 80, 30, "Carrot", 11, self.buy_carrot)

        # Skapa huvudmeny att visa med escape
        pause=Window(*self.center_cords, 200, 130, "Aqua Fish")
        pause.add_button(10, 10, 180, 30, "New Game", 11, self.setup)
        pause.add_button(50, 10, 180, 30, "Open Store", 11, action.open)
        pause.add_button(90, 10, 180, 30, "Exit", 11, window_commands.close_window)
        self.pause = pause # Behövs för att bland annat escape ska fungera

        return [main, event, action, pause]

    def create_bubbles(self, color=(255,255,255,randrange(128,255))):
        list = []
        for i in range(BUBBLE_MAPS):
            list.append(Bubble_map(color=color))
        return list

    def start(self):
        self.window_list[0].close() # Main
        self.window_list[1].open()  # Event
        self.window_list[2].open()  # Action
        self.play()

def main():
    if DEBUG:
        print(f"Starting Aqua Fish v{VERSION}")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
