from queue import SimpleQueue
from arcade import create_text, color, render_text
from vars import SCREEN_HEIGHT, SCREEN_WIDTH

class Logger(SimpleQueue):

    def __init__(self, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT):
        self.message = ["","","","",""]
        self.x = x
        self.y = y

    # Pop the queue and render text
    def update(self):
        if not self.empty():
            text = ""
            while not self.empty():
                self.message.append(self.get())
            l = len(self.message)
            for m in range(l-5, l):
                text += "\n" + self.message[m]
            self.text = create_text(text, color.BLACK, 8)

    def draw(self):
        render_text(self.text, self.x, self.y)
