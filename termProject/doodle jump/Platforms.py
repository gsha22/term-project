'''
Spawns the platforms and gives them properties
'''
from cmu_112_graphics import*

class Platform:
    @staticmethod
    def spawn(lx, hx, ly, hy):
        # spawns a bunch at the beginning, then starts spawning them above screen
        import random
        cx = random.randint(lx, hx)
        cy = random.randint(ly, hy)
        return cx, cy

    @staticmethod
    def createHitbox(cx, cy):
        bottom = cy + 10
        top = cy - 10
        rightSide = cx + 42.5
        leftSide = cx - 65
        return leftSide, top, rightSide, bottom
