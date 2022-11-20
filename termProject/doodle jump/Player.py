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
    
    def xMovements(self, dx):
        self.cx += dx

