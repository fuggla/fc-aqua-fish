"""
Funktioner för att ladda/skapa:
 - Credits
 - Music
 - Bubbles maps
 - Windows
"""

from vars import SCREEN_WIDTH, BUBBLE_MAPS
from arcade import create_text, load_sound, load_texture
from classes.bubble_map import Bubble_map
from classes.window import Window
from random import randrange
from arcade.color import *
from csv import reader

# Läs in och skapa credits text från credits.csv
def load_credits(width=SCREEN_WIDTH, x=0, y=-230, text="AQUA FISH\n\n", color=WHITE, font_size=22):
    with open('credits.csv') as file:
        content = reader(file, delimiter=';')
        for row in content:
            text += f"{row[0]}\n{row[1]}\n\n"
    text = create_text(text, color, font_size, width, "center")
    return text, x, y

# Load music files
def load_music():
    files = [ 
        "assets/music/08-min-mard-ska-klippa-sig-och-skaffa-ett-jobb.wav"
    ]
    music = []
    for f in files:
        music.append(load_sound(f))
    return music

# Ladda in bubblor
def load_bubbles(color=(255,255,255,randrange(128,255))):
    list = []
    for i in range(BUBBLE_MAPS):
        list.append(Bubble_map(color=color))
    return list

# Ladda in alla fönster
def load_windows(game):
    centerx, center_y = game.width / 2, game.height / 2

    # Fönster huvudmeny (Sträcker sig utanför skärmen så det inte kan flyttas)
    main = Window(*game.center_cords, *game.width_height, "Main Menu", bg_color=WHITE)

    # Knappar har en gemensam stil men unik titel, funktion och X-kordinat
    main.add_buttons(
        ( game.width / 2 - 90, 180, 30, 22, WHITE, WHITE, "Lato Light", GRAY ),
        ( "New Game", game.start, center_y - 50 ),
        ( "Credits", game.play_credits, center_y ),
        ( "Exit", exit, center_y + 50 )
    )
    main.open()

    # Fönster för händelser
    event = Window(160, 60, 300, 100, " Events", title_height=20, title_align="left")
    eventhandler = event.add_text(15, 12, 280, 80) # använd game.event.put(text) för nya rader
    print(eventhandler)

    # Fönster för interaktion med spel
    action= Window(80, center_y, 140, 210, " Store", title_height=20, title_align="left")
    action.add_buttons(
        (10, 120, 30),
        ( "Purple Fish", game.buy_pfish, 10 ),
        ( "Blue Small Fish", game.buy_bfish, 50 ),
        ( "Shark", game.buy_shark, 90 ),
        ( "Carrot", game.buy_carrot, 130 ),
        ( "Fishing Rod", game.buy_fishing_rod, 170)
    )

    # Pausefönster att visa med Escape
    pause=Window(*game.center_cords, 200, 130, "Aqua Fish")
    pause.add_buttons(
        ( 10, 180, 30 ),
        ( "Main Menu", game.setup, 10 ),
        ( "Open Store", action.open, 50 ),
        ( "Exit", exit, 90 )
    )

    stats = Window(110, game.height - 80, 200, 100, " Stats", title_height=20, title_align="left")

    return [main, event, action, pause, stats], pause, eventhandler

# Ladda in en fisktexturer
def load_texture_list(type, name, scale):
    t = []
    # Fiskar och hajar har en del sökvägar
    if (type[-4:] == "fish" or type == "shark"):
        img = f"assets/images/fish/{type}/{name}"
        t.append(load_texture(f"{img}1.png", mirrored=True, scale=scale))
        t.append(load_texture(f"{img}2.png", mirrored=True, scale=scale))
        t.append(load_texture(f"{img}1.png", scale=scale))
        t.append(load_texture(f"{img}2.png", scale=scale))
        t.append(load_texture(f"{img}_eat1.png", mirrored=True, scale=scale))
        t.append(load_texture(f"{img}_eat1.png", scale=scale))

    # Shark har en extra ätimation
    if (type == "shark"):
        t.insert(5, load_texture(f"{img}_eat2.png", mirrored=True, scale=scale)) # Direkt efter eat1 mirrored
        t.append(load_texture(f"{img}_eat2.png", scale=scale))

    # Feud
    if (type == "food"):
        img = f"assets/images/{type}/{name}/{name}"
        for i in range(1, 5):
            t.append(load_texture(f"{img}{i}.png", scale=scale))

    return t

# Räkna ut skalor för alla gemensamma texturer
def load_scales():
    from fish_vars import pfish_size, pfish_size_kid, SPRITE_SCALING_PFISH, bfish_size, bfish_size_kid, SPRITE_SCALING_BFISH, shark_size, shark_size_kid, SPRITE_SCALING_SHARK
    from vars import SPRITE_SCALING_POPCORN, SPRITE_SCALING_FISH_HOOK, SPRITE_SCALING_CARROT, SPRITE_SCALING_BLUEBERRY
    return {
        'pfish' : SPRITE_SCALING_PFISH * pfish_size / 8,
        'bfish' : SPRITE_SCALING_BFISH * bfish_size / 8,
        'shark' : SPRITE_SCALING_SHARK * shark_size / 8,
        'pfish_kid' : SPRITE_SCALING_PFISH * pfish_size_kid / 8,
        'bfish_kid' : SPRITE_SCALING_BFISH * bfish_size_kid / 8,
        'shark_kid' : SPRITE_SCALING_SHARK * shark_size_kid / 8,
        'popcorn' : SPRITE_SCALING_POPCORN,
        'hook' : SPRITE_SCALING_FISH_HOOK,
        'carrot' : SPRITE_SCALING_CARROT,
        'blueberry' : SPRITE_SCALING_BLUEBERRY
    }
