'''
Game Physics Classes
    Gravity and Collisions
    also keeping track of total height 
'''

class Gravity:   
    def falling(y, v, a, t):
        dy = v*t + (1/2)*a*t**2
        if v < 2:
            v += a*t
        y += dy
        return (y, v)
    
    def jump():
        return -2

class Collisions:
    def isCollision(x, y, platformHitboxes):
        y = y + 30
        for platform in platformHitboxes:
            if ( (platform[0] <= x <= platform[2]) and
                 (platform[1] <= y <= platform[3]) ):
                return True
        return False
