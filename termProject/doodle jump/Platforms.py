'''
Spawns the platforms and gives them properties
'''


class Platform:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    def spawn(self, cx, cy):
        # spawns a bunch at the beginning, then starts spawning them above screen
        pass 

    def hitbox(self, cx, cy):
        top = cy + 10
        bottom = cy - 10
        rightSide = cx + 42.5
        leftSide = cx - 42.5
        return (leftSide, top, rightSide, bottom)
