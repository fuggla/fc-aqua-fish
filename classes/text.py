from queue import SimpleQueue
from arcade import create_text, color, render_text
from classes.shape import Shape

# Textrutor med ett begränsat antal rader
class Text(Shape, SimpleQueue):

    def __init__(self, x, y, w, h, text="", font_size=8, lines=7, color=(0,0,0), align="left"):
        Shape.__init__(self, x, y, w, h)

        # Nuvarande rader
        self.message = []

        # Maximalt antal rader
        self.lines = lines

        # Text
        self.font_size = font_size
        self.color = color
        self.align = align

        # Förbered för rendering
        self.text = create_text(text, color, font_size, w, align)

    # Rita text
    def draw(self):
        render_text(self.text, self.x, self.y)

    def update(self):
        if not self.empty():
            text = ""
            while not self.empty():
                self.message.insert(0, self.get())
            i = 0
            for m in self.message:
                text = m + "\n" + text
                i += 1
                if (i == self.lines):
                    break
            self.set_text(text)

    def set_text(self, text):
        self.text = create_text(text, self.color, self.font_size, self.w, self.align)
