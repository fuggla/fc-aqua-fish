from csv import reader
from arcade import create_text
from arcade.color import WHITE
from vars import SCREEN_WIDTH

# Läs in och skapa credits text från credits.csv
def create_credits(width=SCREEN_WIDTH, x=0, y=-230, text="AQUA FISH\n\n", color=WHITE, font_size=22):
    with open('credits.csv') as file:
        content = reader(file, delimiter=';')
        for row in content:
            text += f"{row[0]}\n{row[1]}\n\n"
    text = create_text(text, color, font_size, width, "center")
    return text, x, y
