# Hantering av game state
class State():
    # Startmenyn
    def start(self):
        self.state = "start"

    # In game
    def play(self):
        self.state = "playing"

    # In game paus
    def pause(self):
        self.state = "paused"

    def is_paused(self):
        return True if self.state == "paused" else False

    def is_playing(self):
        return True if self.state == "playing" else False

    def is_started(self):
        return True if self.state == "start" else False

    # Ändra läge mellan paused och playing
    def toggle_pause(self):
        self.state = "playing" if self.is_paused() else "paused"
