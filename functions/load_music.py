from arcade import load_sound
# Load music files
def load_music():
    files = [ 
        "assets/music/08-min-mard-ska-klippa-sig-och-skaffa-ett-jobb.wav"
    ]
    music = []
    for f in files:
        music.append(load_sound(f))
    return music
