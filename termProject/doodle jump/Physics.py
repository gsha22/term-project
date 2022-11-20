'''
Game Physics Classes

    = 1/2(g)(t)^2 + vt + h
'''

class Gravity:
    @staticmethod
    def falling(y, v, a, t):
        dy = v*t + (1/2)*a*t**2
        if v < 2:
            v += a*t
        y += dy
        return (y, v)
    
    @staticmethod
    def jump():
        return -2

class Collisions:
    @staticmethod
    def isCollision(x, y, platformHitboxes):
        y = y + 30
        for platform in platformHitboxes:
            if ( (platform[0] <= x <= platform[2]) and
                 (platform[1] <= y <= platform[3]) ):
                return True
        return False
