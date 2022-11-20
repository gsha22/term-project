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
    
    def xMovements(self, xv, t):
        self.cx += xv*t
        self.xv = xv
    
    def shoot(self, cx, cy, t):
        

