VERSION = "0.8.0"

""" Hämta skärmupplösning """
import tkinter
screen = tkinter.Tk()
screen.withdraw()
SCREEN_WIDTH = screen.winfo_screenwidth()
SCREEN_HEIGHT = screen.winfo_screenheight()
FULLSCREEN = True
DIAGNOSE_FISH = False
SKIP_MAIN_MENU = False

""" Bakgrundsbild """
BACKGROUND_IMAGE = "assets/images/background.jpg"
SAND_RATIO = 0.2           # Andel av skärmen täckt av sandbotten

TICK_RATE = 60

""" Egenskaper för morötterna """
SPRITE_SCALING_CARROT = 0.25
carrot_food_value = 1000
carrot_frequency = 1

""" Egenskaper för kroken """
SPRITE_SCALING_FISH_HOOK = 0.15

""" Egenskaper för popcorn """
SPRITE_SCALING_POPCORN = 0.05
popcorn_food_value = 500

""" Egenskaper för blåbär """
SPRITE_SCALING_BLUEBERRY = 0.15
blueberry_food_value = 500

""" Egenskaper för blåbärsplantan """
PLANT_BLUEBERRY_NUMBER = 5
SPRITE_SCALING_PLANT_BLUEBERRY = 0.1
plant_blueberry_grow_rate = 1

""" Egenskaper för förgrundsplantan """
PLANT_FOREGROUND_NUMBER = 5
SPRITE_SCALING_PLANT_FOREGROUND = 0.6

""" Egenskaper för fiskägg """
SCALING_FISH_EGG = 0.15
fish_egg_hatch_age = 1000
fish_egg_disapear_age = 1500

""" Egenskaper för bubbelkartor """
BUBBLE_MAPS = 5             # Antalet bubbelkartor att generera

""" Egenskaper för muspekaren """
SCALING_POINTER = 0.08

"""
Importera debug123.py om den existerar
Filen spåras inte av repo utan är lokal
Ha kvar längst ner, ifall den skriver över några vars
"""
try:
    from debug123 import *
    DEBUG = True
except:
    DEBUG = False
