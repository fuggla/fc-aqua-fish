""" 
Access/Print performance time since the object was created
 
Example: 

# Create new timer
timer = Performance_timer("My timer name")

# Print elapsed time since start
timer.print()
timer.print("Timer progress update message")
print(timer)

# Print elapsed time and a message that notes
# the time measurement as completed/stopped
timer.stop()
timer.stop("the timer is now done")
"""
import time

class Performance_timer():
    def __init__(self, name):
        self.started = time.perf_counter()
        self.name = f"[{name}]:"
        print(self.name, "started")

    def print(self, msg="in progress"):
        print(self, f"({msg})")

    def stop(self, msg="stopped"):
        self.print(msg)

    # Return elapsed time as string with prefix
    def __str__(self):
        return f"{self.name} {(time.perf_counter()-self.started):.4f}s"
