'''
Player class:
    - will keep track of all player movement and y-velocity
'''

class Player:
    def __init__(self, cx, cy, xv, yv):
        self.cx = cx
        self.cy = cy
        self.xv = xv
        self.yv = yv
        self.bv = -2 
    
    def xVel(self, xv):
        self.xv = xv
    
    def playerHitbox(cx, cy):
        lx = cx - 25
        rx = cx + 25
        ty = cy - 30
        by = cy + 30
        return lx, rx, ty, by

