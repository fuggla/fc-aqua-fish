

""" Egenskaper för purple fish """
PFISH_NUMBER = 4
SPRITE_SCALING_PFISH = 0.1

pfish_eager = 5             # Hur ofta byter fiskarna riktning
pfish_hungry = 5            # Hur intresserade är de av mat
pfish_daydream = 10         # Hur ofta de stannar upp och dagdrömmer
pfish_kiss_will = 10        # Hur benägna är de att vilja pussas

pfish_finforce = 6          # Kraften i fenorna
pfish_size = 8              # Påverkan av vattenmotstånd
pfish_mass = 8              # Default är samma som siz<e
pfish_findelay = 20         # Hur ofta viftar de med fenorna

pfish_egg_freq = 1

""" Egenskaper för blue fish """
BFISH_NUMBER = 12
SPRITE_SCALING_BFISH = 0.1

bfish_eager = 10            # Hur ofta byter fiskarna riktning
bfish_hungry = 5            # Hur intresserade är de av mat
bfish_conformity = 10       # Hu måna är fiskarna om att vara som alla andra
bfish_daydream = 5          # Hur ofta de stannar upp och dagdrömmer
bfish_kiss_will = 10        # Hur benägna är de att vilja pussas

bfish_finforce = 6          # Kraften i fenorna
bfish_size = 5              # Påverkan av vattenmotstånd
bfish_mass = 5              # Default är samma som siz<e
bfish_findelay = 10         # Hur ofta viftar de med fenorna

bfish_egg_freq = 1

""" Egenskaper för shark """
SHARK_NUMBER = 2
SPRITE_SCALING_SHARK = 0.8

shark_eager = 10            # Hur ofta byter fiskarna riktning
shark_hungry = 1            # Hur intresserade är de av mat (har ingen effekt nu)
shark_hunt_will = 1         # Hur taggade de är på att börja jaga
shark_daydream = 5          # Hur ofta de stannar upp och dagdrömmer
shark_kiss_will = 10        # Hur benägna är de att vilja pussas

shark_finforce = 16         # Kraften i fenorna
shark_size = 10             # Påverkan av vattenmotstånd
shark_mass = 10             # Default är samma som siz<e
shark_findelay = 25         # Hur ofta viftar de med fenorna
shark_hunting_spirit = 600

shark_egg_freq = 1

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
