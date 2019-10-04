""" 
Access/Print performance time since the object was created
 
Example: 

# Create new timer
timer = Performance_timer("My timer name")

# Print elapsed time since start
timer.print()
# or
print(timer)

# Print elapsed time and a message that notes
# the time measurement as completed/stopped
timer.stop()
"""
import time

class Performance_timer():
    def __init__(self, name):
        self.started = time.perf_counter()
        self.name = f"[{name}]:"
        print(self.name, "started")
        print(self)

    def print(self):
        print(self)

    def stop(self):
        print(self)
        print(self.name, "completed/stopped")

    # Return elapsed time as string with prefix
    def __str__(self):
        return f"{self.name} {(time.perf_counter()-self.started):.4f}s"
