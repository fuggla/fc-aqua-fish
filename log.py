from queue import SimpleQueue
from arcade import create_text, color, render_text
from vars import SCREEN_HEIGHT, SCREEN_WIDTH

class Logger(SimpleQueue):

    def __init__(self, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT, lines=3, color=(0,0,0), size=8, width=200, align="center"):
        self.message = []
        self.x = x
        self.y = y
        self.lines = lines
        self.color = color
        self.size = size
        self.width = width
        self.align = align
        self.set_text("")

    def set_text(self, text):
        self.text = create_text(text, self.color, self.size, self.width, self.align, anchor_x="center", anchor_y="top")

    # Pop the queue and render text
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

    def draw(self):
        render_text(self.text, self.x, self.y)
