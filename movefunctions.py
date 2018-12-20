
import arcade,random

# Rörelsemönster för pfish
def pfishbehaviour(list,sw,sh):
    for fish in list:
        if 0.10*sw < fish.center_x < 0.90*sw:
            fish.relaxed[0] = True
        if 0.10*sh < fish.center_y< 0.90*sh:
            fish.relaxed[1] = True
        if fish.relaxed == [True,True]:
            if fish.pathcounter > 200:
                fish.change_x = random.random() * 2 - 1
                fish.change_y = random.random() * 2 - 1
                fish.pathcounter = random.random()*50
            if random.random() < 0.001:
                fish.change_x = 0
                fish.change_y = 0
                fish.pathcounter = 0
        if fish.center_x > sw * 0.95:
            fish.change_x = -2
            fish.pathcounter = 100
            fish.relaxed[0] = False
        if fish.center_x < sw * 0.05:
            fish.change_x = 2
            fish.pathcounter = 100
            fish.relaxed[0] = False
        if fish.center_y > sh * 0.95:
            fish.change_x = -2
            fish.pathcounter = 100
            fish.relaxed[1] = False
        if fish.center_y < sh * 0.05:
            fish.change_y = 2
            fish.pathcounter = 100
            fish.relaxed[1] = False

        fish.pathcounter += 1

