VERSION = 0.6

""" Hämta skärmupplösning """
import tkinter
screen = tkinter.Tk()
screen.withdraw()
SCREEN_WIDTH = screen.winfo_screenwidth()
SCREEN_HEIGHT = screen.winfo_screenheight()
FULLSCREEN = True
DIAGNOSE_FISH = False

""" Bakgrundsbild """
BACKGROUND_IMAGE = "images/background.png"
SAND_RATIO = 0.18           # Andel av skärmen täckt av sandbotten

TICK_RATE = 60

""" Egenskaper för morötterna """
SPRITE_SCALING_CARROT = 0.3
carrot_food_value = 1000


""" Egenskaper för blåbärsplantan """
PLANT_BLUEBERRY_NUMBER = 5
SPRITE_SCALING_PLANT_BLUEBERRY = 0.7

""" Egenskaper för förgrundsplantan """
PLANT_FOREGROUND_NUMBER = 5
SPRITE_SCALING_PLANT_FOREGROUND = 0.9

""" Egenskaper för fiskägg """
SCALING_FISH_EGG = 0.15
fish_egg_hatch_age = 1000
fish_egg_disapear_age = 1500

""" Egenskaper för bubbelkartor """
BUBBLE_MAPS = 5             # Antalet bubbelkartor att generera

"""
Importera debug.py om den existerar
Filen spåras inte av repo utan är lokal
Ha kvar längst ner, ifall den skriver över några vars
"""
try:
    from debug import *
    DEBUG = True
except:
    DEBUG = False
