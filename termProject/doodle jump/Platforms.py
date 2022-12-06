'''
Spawns the platforms and gives them properties
'''
from cmu_112_graphics import*
import random


class Platform:
    def createInitialMap(platformList, numPlatforms, max_y_distance):
        if len(platformList) == numPlatforms:
            return platformList
        else:
            highestY = 1000
            for platform in platformList:
                if platform[1] < highestY:
                    highestY = platform[1]
            lx, hx = 50, 550
            ly = highestY - 20
            hy = highestY - max_y_distance
            cx = random.randint(lx, hx)
            cy = random.randint(hy, ly)
            platformList.append([cx, cy])
            return Platform.createInitialMap(platformList, numPlatforms, max_y_distance)


    def infiniteSpawner(platformList, numPlatforms, max_y_distance, difficulty): 
        if len(platformList) == numPlatforms:
            return platformList
        else:
            highestY = 0
            for platform in platformList:
                if platform[1] < highestY:
                    highestY = platform[1]
            lx, hx = 50, 550
            ly = highestY - 20
            if difficulty:
                ly = highestY-100
            hy = highestY - max_y_distance
            cx = random.randint(lx, hx)
            cy = random.randint(hy, ly)
            platformList.append([cx, cy])
            return Platform.infiniteSpawner(platformList, numPlatforms, max_y_distance, difficulty)
    
    def basicSpawn(lx, hx, ly, hy):
        cx = random.randint(lx, hx)
        cy = random.randint(ly, hy)
        return cx, cy

    def isLegalPlatform(cx, cy, platformList):
        if len(platformList) == 0:
            return True
        highestY = 1000
        for platform in platformList:
            if platform[1] < highestY:
                highestY = platform[1]
        if (50 < abs(cy - highestY) < 150) and (abs(cx - platform[0]) > 100):
            return True
        else:
            return False

    def needsMorePlatforms(platformList):
        for platform in platformList:
            if platform[1] < 0:
                return False
        return True

    def createHitbox(cx, cy):
        bottom = cy + 10
        top = cy - 10
        rightSide = cx + 42.5
        leftSide = cx - 65
        return leftSide, top, rightSide, bottom
