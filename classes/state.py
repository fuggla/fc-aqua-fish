# Hantering av game state
class State():
    # Ändra läge mellan paused och playing
    def toggle_pause(self):
        self.state = "playing" if self.is_paused() else "paused"

    # Ändra state till playing
    def play(self):
        self.state = "playing"

    # Ändra state till playing
    def play(self):
        self.state = "paused"

    # Return true om spelet är pausat
    def is_paused(self):
        return True if self.state == "paused" else False

    # Return true om spelet spelas
    def is_playing(self):
        return True if self.state == "playing" else False
