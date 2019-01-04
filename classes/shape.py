# Klass för att rita diverse former
class Shape():

    def __init__(self, x, y, w, h):
        # Position och storlek
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.height = h
        self.width = w

        # Storlek och position
        self.size= [w, h]
        self.pos = [x, y]

    def set_position(self, pos):
        self.pos = pos

    def get_position(self):
        return self.x, self.y

    # Flytta relativt
    def move(self, x, y):
        self.x += x
        self.y += y
