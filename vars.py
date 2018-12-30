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

""" Egenskaper för fiskägg """
SCALING_FISH_EGG = 0.15

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
    print("Debug enabled")
except:
    DEBUG = False
