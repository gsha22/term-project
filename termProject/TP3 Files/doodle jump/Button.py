'''
Button class
'''

class CircleButton:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    def buttonHitbox(self):
        lx = self.cx - 70
        rx = self.cx + 40
        ty = self.cy - 30
        by = self.cy + 30
        return lx, rx, ty, by

class RectangleButton:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    def buttonHitbox(self):
        lx = self.cx - 70
        rx = self.cx + 70
        ty = self.cy - 20
        by = self.cy + 20
        return lx, rx, ty, by