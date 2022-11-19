'''
Player class:
    - will keep track of all player movement and y-velocity
'''

class Player:
    def __init__(self, cx, cy, yv):
        self.cx = cx
        self.cy = cy
        self.yv = yv
    
    def xMovements(self, dcx):
        self.cx += dcx

    