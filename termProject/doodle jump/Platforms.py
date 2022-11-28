'''
Spawns the platforms and gives them properties
'''
from cmu_112_graphics import*
import random


class Platform:
    @staticmethod
    def createInitialMap(platformList, numPlatforms, max_y_distance):
        print(platformList)
        if len(platformList) == numPlatforms:
            return platformList
        else:
            highestY = 1000
            for platform in platformList:
                if platform[1] < highestY:
                    highestY = platform[1]
            lx, hx = 100, 500
            ly = highestY - 20
            hy = highestY - max_y_distance
            cx = random.randint(lx, hx)
            cy = random.randint(ly, hy)
            platformList.append([cx, cy])
            return Platform.createInitialMap(platformList, numPlatforms, max_y_distance)



    @staticmethod
    def spawn(lx, hx, ly, hy): 
        # spawns a bunch at the beginning, then starts spawning them above screen
        cx = random.randint(lx, hx)
        cy = random.randint(ly, hy)
        return cx, cy

    @staticmethod
    def isLegalPlatform(cx, cy, platformList):
        if len(platformList) == 0:
            return True
        highestY = 1000
        for platform in platformList:
            if platform[1] < highestY:
                highestY = platform[1]
        if (0 < abs(cy - highestY) < 150) and (abs(cx - platform[0]) > 100):
            return True
        else:
            return False

    @staticmethod
    def createHitbox(cx, cy):
        bottom = cy + 10
        top = cy - 10
        rightSide = cx + 42.5
        leftSide = cx - 65
        return leftSide, top, rightSide, bottom
