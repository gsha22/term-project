'''
Enemy Class:
    spawns goofy looking monsters, if you touch them you fall and lose
'''
import random

class Monster:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    def hitbox(self):
        lx = self.cx - 40
        rx = self.cx + 40
        ty = self.cy - 40
        by = self.cy + 40
        return lx, rx, ty, by 
    
    def spawnEnemy():
        lx, hx = 50, 550
        cy = -200
        cx = random.randint(lx, hx)
        return cx, cy

