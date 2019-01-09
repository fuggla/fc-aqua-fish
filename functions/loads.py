from classes.bubble_map import Bubble_map
from csv import reader
from arcade import create_text, load_sound
from arcade.color import WHITE
from vars import SCREEN_WIDTH, BUBBLE_MAPS
from random import randrange

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

def load_bubbles(color=(255,255,255,randrange(128,255))):
    list = []
    for i in range(BUBBLE_MAPS):
        list.append(Bubble_map(color=color))
    return list
