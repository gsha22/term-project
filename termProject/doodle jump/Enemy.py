'''
Enemy Class:
    spawns goofy looking monsters, if you touch them you fall and lose
'''
import random

class Monster:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    def enemyHitbox(cx, cy):
        lx = cx - 30
        rx = cx + 30
        ty = cy - 40
        by = cy + 40
        return lx, rx, ty, by
    
    def spawnEnemy():
        lx, hx = 50, 550
        cy = -200
        cx = random.randint(lx, hx)
        return cx, cy

