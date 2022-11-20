'''
Spawns the platforms and gives them properties
'''
from cmu_112_graphics import*

class Platform:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy

    @staticmethod
    def spawn():
        # spawns a bunch at the beginning, then starts spawning them above screen
        import random
        cx = random.randint(50, 550)
        cy = random.randint(50, 950)
        return cx, cy

    @staticmethod
    def createHitbox(cx, cy):
        bottom = cy + 10
        top = cy - 10
        rightSide = cx + 42.5
        leftSide = cx - 65
        return leftSide, top, rightSide, bottom
