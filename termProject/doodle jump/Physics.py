'''
Game Physics Classes

    = 1/2(g)(t)^2 + vt + h
'''

class Gravity:
    @staticmethod
    def falling(y, v, a, t):
        dy = v*t + (1/2)*a*t**2
        v += (a*t)/100 
        y += (dy)/100
        # if isCollision(y):
        #     return (y, -v, a)
        return (y, v, a)

class Collisions:
    @staticmethod
    def collide(x, y, v, t, platformHitboxes):
        y = y + 15
        for platform in platformHitboxes:
            if ( platform[0] <= x <= platform[2] and
                 platform[1] <= y <= platform[3] ):
                v = -v 
                t = 0
                return (v, t)
