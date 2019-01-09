"""
Funktioner för att ladda/skapa:
 - Credits
 - Music
 - Bubbles maps
 - Windows
"""

from vars import SCREEN_WIDTH, BUBBLE_MAPS
from arcade import create_text, load_sound
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
    event = Window(110, 60, 200, 100, " Events", title_height=20, title_align="left")
    game.event = event.add_text(15, 12, 180, 80) # använd game.event.put(text) för nya rader

    # Fönster för interaktion med spel
    action= Window(60, center_y, 100, 170, " Store", title_height=20, title_align="left")
    action.add_buttons(
        (10, 80, 30),
        ( "Pfish", game.buy_pfish, 10 ),
        ( "Bfish", game.buy_bfish, 50 ),
        ( "Shark", game.buy_shark, 90 ),
        ( "Carrot", game.buy_carrot, 130 )
    )

    # Pausefönster att visa med Escape
    pause=Window(*game.center_cords, 200, 130, "Aqua Fish")
    pause.add_buttons(
        ( 10, 180, 30 ),
        ( "New Game", game.setup, 10 ),
        ( "Open Store", action.open, 50 ),
        ( "Exit", exit, 90 )
    )
    game.pause = pause # Behövs för att bland annat escape ska fungera

    return [main, event, action, pause]
