# Klass för att rita diverse former
class Shape():

    def __init__(self, x, y, width, height):
        # Position och storlek
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    # Flytta relativt
    def move(self, x, y):
        self.x += x
        self.y += y
