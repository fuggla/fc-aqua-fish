import tkinter
VERSION = 0.5

# För att ta fram upplösning
screen = tkinter.Tk()
screen.withdraw()
SCREEN_WIDTH = screen.winfo_screenwidth()
SCREEN_HEIGHT = screen.winfo_screenheight()

SAND_RATIO = 0.18      # Andel av skärmen täckt av sandbotten

TICK_RATE = 60

""" Egenskaper för purple fish """
PFISH_NUMBER = 1
SPRITE_SCALING_PFISH = 0.1

pfish_eager = 5             # Hur ofta byter fiskarna riktning
pfish_hungry = 500            # Hur intresserade är de av mat
pfish_daydream = 10         # Hur ofta de stannar upp och dagdrömmer

pfish_finforce = 6          # Kraften i fenorna
pfish_size = 8              # Påverkan av vattenmotstånd
pfish_mass = 8              # Default är samma som siz<e
pfish_findelay = 20         # Hur ofta viftar de med fenorna

""" Egenskaper för blue fish """
BFISH_NUMBER = 0
SPRITE_SCALING_BFISH = 0.1

bfish_eager = 10            # Hur ofta byter fiskarna riktning
bfish_hungry = 5            # Hur intresserade är de av mat (har ingen effekt nu)
bfish_conformity = 10       # Hu måna är fiskarna om att vara som alla andra
bfish_daydream = 5          # Hur ofta de stannar upp och dagdrömmer

bfish_finforce = 6          # Kraften i fenorna
bfish_size = 5              # Påverkan av vattenmotstånd
bfish_mass = 5              # Default är samma som siz<e
bfish_findelay = 10         # Hur ofta viftar de med fenorna

""" Egenskaper för morötterna """
SPRITE_SCALING_CARROT = 0.3
carrot_food_value = 100

""" Egenskaper för bubbelkartor """
BUBBLE_MAPS = 5             # Antalet bubbelkartor att generera
