"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types, math, csv
from arcade import SpriteList, load_texture, start_render, draw_texture_rectangle, check_for_collision_with_list, window_commands, draw_rectangle_filled, play_sound, render_text
from random import randrange
from arcade.key import *
from arcade.color import *
from classes.state import State
from classes.purple_fish import PfishSprite
from classes.blue_small_fish import BfishSprite
from classes.shark import SharkSprite
from classes.carrot import CarrotSprite
from classes.blueberry import BlueberrySprite
from classes.fish_hook import FishHookSprite
from classes.popcorn import PopcornSprite
from classes.plant_blueberry import PlantBlueberry
from classes.plant_foreground import PlantForeground
from classes.fish_egg import FishEggSprite
from classes.window import Window, Button, Text
from classes.timer import Performance_timer
from classes.bubble_map import Bubble_map
from classes.fade import Fade
from classes.fps import Fps
from classes.pointer import Pointer
from functions.diagnose_name_gender_attraction_health import diagnose_name_gender_attraction_health
from functions.diagnose_name_gender_health_hungry import diagnose_name_gender_health_hungry
from functions.loads import *
from vars import *
from fish_vars import PFISH_NUMBER, BFISH_NUMBER, SHARK_NUMBER, pfish_size, pfish_size_kid, SPRITE_SCALING_PFISH, \
    bfish_size, bfish_size_kid, SPRITE_SCALING_BFISH, shark_size


class MyGame(arcade.Window, State):

    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=FULLSCREEN)

        self.frame_count = 0
        self.show_windows = True
        self.background = None
        self.center_cords = (width // 2, height // 2)
        self.width_height = (width, height)

        # Sätt spritelistor och vanliga listor till none
        self.sprite_list_names = ["pfish", "bfish", "shark", "carrot", "blueberry", "popcorn", "fish_hook",
                                   "plant_blueberry", "plant_foreground", "fish_egg", "all_sprite", "pointer" ]
        self.standard_list_names = ["window", "bubble", "bubble_main", "berry_info", "music"]
        for l in self.sprite_list_names + self.standard_list_names:
            setattr(self, f"{l}_list", None)

        # Listor med texturer
        self.textures_pfish_purple = []
        self.textures_pfish_purple_kid = []
        self.textures_bfish_blue = []
        self.textures_bfish_blue_kid = []

        # Listor med information om fiskarna
        self.pfish_info = []
        self.bfish_info = []
        self.shark_info = []

        # Den sprite som flyttas med musen
        self.dragged_sprite = None

    def setup(self):
        self.timer = Performance_timer("Loading started")

        # Skapa listor
        for l in self.sprite_list_names:
            setattr(self, f"{l}_list", SpriteList())
        self.berry_info_list = []
        self.window_list, self.pause, self.event = load_windows(self)
        self.bubble_list = load_bubbles()
        self.bubble_main_list = load_bubbles((0,0,0,randrange(64,192)))
        self.music_list = load_music()

        """ Skapa alla fiskar """
        # Ladda in texturer
        self.load_textures()

        # Skapa purple_fish
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite(self.textures_pfish_purple, self.textures_pfish_purple_kid, self.carrot_list,
                                self.popcorn_list, self.pfish_list)
            self.pfish_list.append(pfish)
            self.all_sprite_list.append(pfish)

        # Skapa blue_small_fish
        for i in range(BFISH_NUMBER):
            bfish = BfishSprite(self.textures_bfish_blue, self.textures_bfish_blue_kid, self.carrot_list,
                                self.blueberry_list, self.popcorn_list, self.bfish_list, self.shark_list)
            self.bfish_list.append(bfish)
            self.all_sprite_list.append(bfish)

        # Skapa shark
        for i in range(SHARK_NUMBER):
            shark = SharkSprite(self.bfish_list, self.popcorn_list, self.shark_list, self.event)
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
        self.set_mouse_visible(False)
        self.pointer_list.use_spatial_hash = False
        self.pointer_list.append(Pointer())
        self.pointer = self.pointer_list[0]

        # Setup klar. Använd timer för att vänta med toning
        # Tona in grafik över ~2 sekunder
        self.fade = Fade(a=255, time=2, pause=self.timer.done("Loading done"))
        self.fade.start_in()

        if SKIP_MAIN_MENU:
            self.start()
        else:
            self.credits_text, self.credits_x, self.credits_y, self.credits_settings = load_credits()
            self.state_main_menu()

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        start_render()

        if self.is_playing() or self.is_paused():
            # Rita bakgrund
            draw_texture_rectangle(*self.center_cords, *self.width_height, self.background)

            for b in self.bubble_list:
                b.draw()

            self.plant_blueberry_list.draw()
            self.blueberry_list.draw()
            self.draw_fishing_lines()
            self.fish_hook_list.draw()
            self.popcorn_list.draw()
            self.fish_egg_list.draw()
            self.all_sprite_list.draw()
            self.plant_foreground_list.draw()

        # "DIAGNOSE_FISH = True" skriver ut information om varje fisk
            if DIAGNOSE_FISH:
                self.diagnose_all_fish()

            if self.show_windows:
                for w in self.window_list:
                    w.draw()

        elif self.is_main_menu():
            self.draw_main_menu()

        elif self.is_credits():
            self.draw_credits()

        self.fade.draw()

        # Rita FPS uppe i högra hörnet
        self.fps_counter.draw()

        # Rita ut muspekaren
        if self.is_credits() == False:
            self.pointer_list.draw()

    def update(self, dt):

        """ Uppdatera all när spelet är igång """
        if self.is_playing():
            self.plant_blueberry_list.update()
            self.blueberry_list.update()
            self.fish_egg_list.update()
            self.all_sprite_list.update()
            self.fish_hook_list.update()
            self.popcorn_list.update()
            self.plant_foreground_list.update()

            """ Släpp ner morötter ibland """
            self.random_carrot_drop()

            """ Här stegas alla fiskar och föremål igenom för interaktion med andra objekt """
            self.interactions_pfish()
            self.interactions_bfish()
            self.interactions_shark()

            self.interactions_fishing_rod()
            self.interactions_egg()
            self.interactions_plant_blueberry()

            """ Flytta bubblor """
            for b in self.bubble_list:
                b.update(dt)

            """ Uppdatera eventruta """
            if self.event.message_received():
                self.event.update()

        elif self.is_main_menu():
            self.update_menu_bubbles(dt)

        elif self.is_credits():
            self.update_credits(dt)

        self.fade.update(dt)
        self.fps_counter.calculate(dt)
        self.frame_count += 1

    def on_key_release(self, key, key_modifiers):
        if (key == Q): # Avsluta
            exit()
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
        if self.dragged_sprite:                                      # Om det finns dragna sprites
            self.dragged_sprite.drag_sprite(x, y, dx, dy)            # Så flytta dem och spara pekarens hastighet

        # Här flyttas muspekaren då musen flyttas.
        self.pointer.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        for w in self.get_open_windows():
            w.on_mouse_press(x, y)
            if w.dragging:
                self.pointer.grab()
                return
        for sprite in self.all_sprite_list:                             # Stega igenom alla fiskar och morötter
            if sprite.is_mouse_on(self.pointer):                        # Kolla ifall de är i kontakt med pekaren
                self.dragged_sprite = sprite
                self.dragged_sprite.dragged = True
                self.pointer.grab()
                return

    def on_mouse_release(self, x, y, button, key_modifiers):
        if self.is_credits():
            return
        for w in self.get_open_windows():
            w.on_mouse_release(x, y)
        if self.dragged_sprite:
            self.dragged_sprite.release()
            self.dragged_sprite.dragged = False
            self.dragged_sprite = None
        self.pointer.point()

        # Alltid spela spel när pausmenyn är stängs
        if self.is_paused() and self.pause.is_closed():
            self.play()

    """ 
    
    
    Metoder utanför arcadestrukturen:
    (i bokstavsordning)
    
    
    """

    def buy_bfish(self):
        self.buy_fish("bfish")

    def buy_carrot(self):
        carrot = CarrotSprite(setspeed_y=-20)
        self.carrot_list.append(carrot)
        self.all_sprite_list.append(carrot)
        self.event.put("Bought carrot")

    def buy_fish(self, name):
        fish = None
        if (name == "pfish"):
            color = ["purple", "orange", "green"]
            fish = PfishSprite(self.textures_pfish_purple, self.textures_pfish_purple_kid, self.carrot_list,
                               self.popcorn_list, self.pfish_list, color=color[random.randrange(2)],
                               setpos_y=self.height, setspeed_y=-30)
            self.pfish_list.append(fish)
        elif (name == "bfish"):
            fish = BfishSprite(self.textures_bfish_blue, self.textures_bfish_blue_kid, self.carrot_list, self.blueberry_list, self.popcorn_list, self.bfish_list, self.shark_list, setpos_y=self.height, setspeed_y=-30)
            self.bfish_list.append(fish)
        elif (name == "shark"):
            fish = SharkSprite(self.bfish_list, self.popcorn_list, self.shark_list, setpos_y = self.height, setspeed_y=-30, event=self.event)
            self.shark_list.append(fish)

        # Done and done
        self.all_sprite_list.append(fish)
        self.event.put(f"Bought {name} {fish.get_name()}")

    def buy_fishing_rod(self):
        fish_hook = FishHookSprite(self.fish_hook_list)
        if fish_hook.not_placed:
            self.event.put("No room for fishing rod")
        else:
            self.fish_hook_list.append(fish_hook)

            popcorn = PopcornSprite(fish_hook)
            self.popcorn_list.append(popcorn)

            self.event.put("Bought fishing rod")

    def buy_pfish(self):
        self.buy_fish("pfish")

    def buy_shark(self):
        self.buy_fish("shark")

    def draw_credits(self):
        if self.fade.is_fading_out():
            self.draw_main_menu()
        draw_text(self.credits_text, self.credits_x, self.credits_y, *self.credits_settings)

    def draw_main_menu(self):
        self.window_list[0].draw()
        for b in self.bubble_main_list:
            b.draw()

    def diagnose_all_fish(self):
        # Metod för att skriva ut information om alla fiskar
        if self.frame_count % 60 == 0:                                                      # Samla bara infon 1 g/s
            self.get_fish_info()                                                            # Anropa metod
        if self.pfish_list:                                                                 # Det undvik krash
            diagnose_name_gender_attraction_health(self.pfish_list, self.pfish_info)
        if self.bfish_list:
            diagnose_name_gender_attraction_health(self.bfish_list, self.bfish_info)
        if self.shark_list:
            diagnose_name_gender_attraction_health(self.shark_list, self.shark_info)

    def draw_fishing_lines(self):
        for hook in self.fish_hook_list:
            x1 = hook.center_x - 2
            y1 = hook.center_y + 31
            x2 = hook.center_x - 2
            y2 = SCREEN_HEIGHT * 1.1
            arcade.draw_line(x1, y1, x2, y2, arcade.color.BLACK)

    def get_fish_info(self):
        self.pfish_info = []
        for i in range(len(self.pfish_list)):
            self.pfish_info.append([self.pfish_list[i].name_gender[0], self.pfish_list[i].name_gender[1],
                                    self.pfish_list[i].attraction, self.pfish_list[i].health])
        self.bfish_info = []
        for i in range(len(self.bfish_list)):
            self.bfish_info.append([self.bfish_list[i].name_gender[0], self.bfish_list[i].name_gender[1],
                                    self.bfish_list[i].attraction, self.bfish_list[i].health])
        self.shark_info = []
        for i in range(len(self.shark_list)):
            self.shark_info.append([self.shark_list[i].name_gender[0], self.shark_list[i].name_gender[1],
                                    self.shark_list[i].attraction, self.shark_list[i].health])

    def get_open_windows(self, dragged_only=False):
        # Hämta alla tillgängliga fönster
        open_windows = []
        if self.show_windows:
            for w in self.window_list:
                if w.is_dragged():
                    return [ w ]
                elif w.is_open() and not dragged_only:
                    open_windows.append(w)
        return open_windows

    def interactions_bfish(self):
        """ Stega igenom bfish """
        for fish in self.bfish_list:
            # Ätalgoritm för blue small fish
            hit_list = check_for_collision_with_list(fish, self.carrot_list)
            hit_list2 = check_for_collision_with_list(fish, self.blueberry_list)
            hit_list3 = check_for_collision_with_list(fish, self.popcorn_list)
            for hit in hit_list2:
                hit_list.append(hit)
            for hit in hit_list3:
                hit_list.append(hit)

            if len(hit_list) == 0 and fish.iseating > 0:
                fish.iseating -= 1
            # Om fisken lever och det finns en morot äter fisken på den
            if hit_list and not fish.disturbed:
                fish.eat_food(hit_list[0], 1)  # 1 är hur mycket de äter varje tugga

            # Lägg ägg ifall fisken är gravid
            if fish.ready_to_lay_egg:
                fish.pregnant = False
                fish.ready_to_lay_egg = False
                fish.laid_eggs += 1
                egg = FishEggSprite(fish, "small")
                self.fish_egg_list.append(egg)
                self.event.put(fish.get_name() + " laid an egg")

    def interactions_egg(self):
        """ Stega igenom äggen """
        for egg in self.fish_egg_list:
            if egg.age == egg.hatch_age:  # ägget kläcks efter en viss tid
                egg.set_texture(1)
                if egg.origin == "pfish":
                    # Kläck en pfish om ägget kom från pfish
                    pfish = PfishSprite(self.textures_pfish_purple, self.textures_pfish_purple_kid, self.carrot_list,
                                        self.popcorn_list, self.pfish_list, setpos_x=egg.center_x,
                                        setpos_y=egg.center_y, size=pfish_size_kid)
                    self.pfish_list.append(pfish)
                    self.all_sprite_list.append(pfish)
                if egg.origin == "bfish":
                    # Kläck en bfish om ägget kom från bfish
                    bfish = BfishSprite(self.textures_bfish_blue, self.textures_bfish_blue_kid, self.carrot_list,
                                        self.blueberry_list, self.popcorn_list, self.bfish_list, self.shark_list,
                                        setpos_x=egg.center_x, setpos_y=egg.center_y, size=bfish_size_kid)
                    self.bfish_list.append(bfish)
                    self.all_sprite_list.append(bfish)
                if egg.origin == "shark":
                    # Kläck en shark om ägget kom från haj
                    shark = SharkSprite(self.bfish_list, self.popcorn_list, self.shark_list, setpos_x=egg.center_x,
                                        setpos_y=egg.center_y, event=self.event, size=pfish_size * 0.6)
                    self.shark_list.append(shark)
                    self.all_sprite_list.append(shark)
            if egg.age > egg.disapear_age:  # Ta bort äggresterna efter ett tag
                egg.kill()
            egg.age += 1

    def interactions_fishing_rod(self):
        """" Stega igenom hook och popcorn """
        for hook in self.fish_hook_list:
            # Kolla vilka fiskar som är i kontakt med kroken
            pfish_hook_list = check_for_collision_with_list(hook, self.pfish_list)
            bfish_hook_list = check_for_collision_with_list(hook, self.bfish_list)
            shark_hook_list = check_for_collision_with_list(hook, self.shark_list)

            # Spara fiskarna som kontaktar kroken och äter i en lista
            fish_hook_list = []
            for fish in pfish_hook_list:
                if fish.iseating > 0:
                    fish_hook_list.append(fish)
            for fish in bfish_hook_list:
                if fish.iseating > 0:
                    fish_hook_list.append(fish)
            for fish in shark_hook_list:
                if fish.iseating > 0:
                    fish_hook_list.append(fish)

            if fish_hook_list:
                # Plocka ut en stackare från listan
                index = random.randrange(len(fish_hook_list))
                fish = fish_hook_list[index]

                # Olika sannolikhet för olika fiskar
                if fish.type == "pfish":
                    prob = 15
                elif fish.type == "bfish":
                    prob = 5
                else:
                    prob = 200

                # fisken fastnar ifall slumpfaktorn slår in
                if random.randrange(1000) < prob and not hook.has_fish:
                    hook.has_fish = True                    # Kroken har en fisk
                    fish.hooked(hook)                       # Fisken är krokad på kroken
                    self.event.put(f"You caught a {fish.type} named {fish.get_name()}")

            # Ge upp ifall ingen fisk har fastnat och popcornet är slut
            if not check_for_collision_with_list(hook, self.popcorn_list):
                hook.no_fish()

    def interactions_pfish(self):
        """" Stega igenom pfish """
        #food_sprite_list = self.carrot_list
        #for popcorn in self.popcorn_list:
        #    food_sprite_list.append(popcorn)

        for fish in self.pfish_list:
            # Samla ihop all mat
            hit_list = check_for_collision_with_list(fish, self.carrot_list)
            hit_list2 = check_for_collision_with_list(fish, self.popcorn_list)
            for hit in hit_list2:
                hit_list.append(hit)

            if len(hit_list) == 0 and fish.iseating > 0:
                fish.iseating -= 1
            # Om fisken lever och det finns en morot äter fisken på den
            if hit_list and not fish.disturbed:
                fish.eat_food(hit_list[0], 5)  # 5 är hur mycket de äter varje tugga

            # Lägg ägg ifall fisken är gravid
            if fish.ready_to_lay_egg:
                fish.pregnant = False
                fish.ready_to_lay_egg = False
                fish.laid_eggs += 1
                egg = FishEggSprite(fish, "medium")
                self.fish_egg_list.append(egg)
                self.event.put(fish.get_name() + " laid an egg")

    def interactions_plant_blueberry(self):
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

    def interactions_shark(self):
        """ Stega igenom hajarna """
        for fish in self.shark_list:
            # Ätalgoritm för shark
            if fish.iseating > 0:
                fish.iseating -= 1
            hit_list = check_for_collision_with_list(fish, self.bfish_list)
            # Om fisken lever och det finns en blue small fish äter fisken den
            if hit_list and not fish.disturbed:
                fish.eat_fish(hit_list[0])

            # Ätalgoritm för shark
            if fish.iseating > 0:
                fish.iseating -= 1
            hit_list = check_for_collision_with_list(fish, self.popcorn_list)
            # Om fisken lever och det finns ett popcorn fish äter fisken det
            if hit_list and not fish.disturbed:
                fish.eat_fish(hit_list[0])

            # Lägg ägg ifall fisken är gravid
            if fish.ready_to_lay_egg:
                fish.pregnant = False
                fish.ready_to_lay_egg = False
                fish.laid_eggs += 1
                egg = FishEggSprite(fish, "large")
                self.fish_egg_list.append(egg)
                self.event.put(fish.get_name() + " laid an egg")

    def load_textures(self):
        """ Ladda alla texturer så de kan skickas till objekten """
        # Pfish
        img = f"assets/images/fish/pfish/purple"
        scale_factor = SPRITE_SCALING_PFISH * pfish_size / 8
        self.textures_pfish_purple = []
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish1.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish2.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish1.png", scale=scale_factor))
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish2.png", scale=scale_factor))
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish_eat.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple.append(arcade.load_texture(f"{img}_fish_eat.png", scale=scale_factor))

        img = f"assets/images/fish/pfish/purple"
        scale_factor = SPRITE_SCALING_PFISH * pfish_size_kid / 8
        self.textures_pfish_purple_kid = []
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish1.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish2.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish1.png", scale=scale_factor))
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish2.png", scale=scale_factor))
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish_eat.png", mirrored=True, scale=scale_factor))
        self.textures_pfish_purple_kid.append(arcade.load_texture(f"{img}_fish_eat.png", scale=scale_factor))

        # Bfish
        scale_factor = SPRITE_SCALING_BFISH * bfish_size / 8
        img = f"assets/images/fish/bfish/blue_small"
        self.textures_bfish_blue = []
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish1.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish2.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish1.png", scale=scale_factor))
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish2.png", scale=scale_factor))
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish_eat.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue.append(arcade.load_texture(f"{img}_fish_eat.png", scale=scale_factor))

        scale_factor = SPRITE_SCALING_BFISH * bfish_size_kid / 8
        img = f"assets/images/fish/bfish/blue_small"
        self.textures_bfish_blue_kid = []
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish1.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish2.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish1.png", scale=scale_factor))
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish2.png", scale=scale_factor))
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish_eat.png", mirrored=True, scale=scale_factor))
        self.textures_bfish_blue_kid.append(arcade.load_texture(f"{img}_fish_eat.png", scale=scale_factor))

    def play_credits(self):
        if self.is_credits() == False:
            self.fade = Fade(a=255, time=4)
            self.fade.start_out()
            play_sound(self.music_list[0])
            self.credits()

    def random_carrot_drop(self):
        """ Skapa en morot med sannolikheten [carrot_frequency] på 1000 varje frame """
        if random.randrange(1000) < carrot_frequency:
            carrot = CarrotSprite(setspeed_y=-20)
            self.carrot_list.append(carrot)
            self.all_sprite_list.append(carrot)

    def start(self):
        main, event, action = 0, 1, 2
        self.window_list[main].close()
        self.window_list[event].open()
        self.window_list[action].open()
        self.play()

    def update_credits(self, dt):
        if self.fade.is_fading_out():
            self.update_menu_bubbles(dt)
        self.credits_y += 20 * dt

    def update_menu_bubbles(self, dt):
        for b in self.bubble_main_list:
            b.update(dt)


def main():
    if DEBUG:
        print(f"Starting Aqua Fish v{VERSION}")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
