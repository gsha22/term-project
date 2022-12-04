''' 
Main file: Runs all classes and game
'''

#imports
from cmu_112_graphics import *
import math
import random

from Physics import Gravity
from Physics import Collisions

from Platforms import Platform

from Player import Player
from Button import CircleButton
from Enemy import Monster

def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")
    app.normaldoodle = app.scaleImage(app.doodle, 2/3)
    app.doodle = app.normaldoodle
    app.rightDoodle = app.doodle.transpose(Image.FLIP_LEFT_RIGHT)

    app.shooter = app.loadImage("shooting_doodle.png")
    app.shooter = app.scaleImage(app.shooter, 2/3)

    app.blueMonster = app.loadImage("blue_monster.png")
    app.blueMonster = app.scaleImage(app.blueMonster, 3/5)
    app.monsterdx = 4

    app.platform = app.loadImage("green_platform.png")
    app.platform = app.scaleImage(app.platform, 2/3)
    app.num_green_platforms = 5
    app.max_green_y_distance = 100

    app.bluePlatform = app.loadImage("blue_platform.png")
    app.bluePlatform = app.scaleImage(app.bluePlatform, 2/3)
    app.bluedx = 3

    app.bullet = app.loadImage("bullet.png")
    app.bullet = app.scaleImage(app.bullet, 2/3)

    #BACKGROUND
    app.background = app.loadImage("background.png")
    app.background = app.scaleImage(app.background, 4/3)

    # dazed animation 
    app.dazed1 = app.loadImage("stars1.png")
    app.dazed2 = app.loadImage("stars2.png")
    app.dazed3 = app.loadImage("stars3.png")
    app.dazedList = [app.dazed1, app.dazed2, app.dazed3]
    app.dazedIndex = 0
    app.dazedImg = app.dazedList[app.dazedIndex]

    app.player = Player(300, 400, 0, 0)

    app.a = 0.01
    app.time = 0
    app.gameSeconds = 0
    app.waveTime = 0


    app.platforms = []
    app.hitboxes = []

    app.bluePlatforms = []
    app.blueHitboxes = []

    app.bullets = []

    app.monsterList = []

    app.timerDelay = 1

    app.score = 0

    app.mouseX = 0
    app.mouseY = 0

    app.dazed = False

    # Starting Menu
    app.startingMenu = True
    app.startingDoodle = Player(150, 600, 0, 0)

    app.title = app.loadImage("doodle-jump.png")
    app.playButton = app.loadImage("playButton.png")
    app.playButton = app.scaleImage(app.playButton, 2/3)

    app.pressedPB = app.loadImage("playButton_on.png")
    app.pressedPB = app.scaleImage(app.pressedPB, 2/3)

    app.playButtonButton = CircleButton(400, 500)
    app.pbIsPressed = False

    #currently playing the game
    app.playingGame = False

    # Game Over
    app.gameOver = False
    app.gameOverX = 300
    app.gameOverY = 1550
    app.stopGravity = False
    app.playAgain = app.loadImage("playagain.png")
    app.playAgain = app.scaleImage(app.playAgain, 2/3)
    app.playAgainOn = app.loadImage("playagain_on.png")
    app.playAgainOn = app.scaleImage(app.playAgainOn, 2/3)
    app.pabX = 300
    app.pabY = 1700
    app.playAgainButton = CircleButton(app.pabX, app.pabY)
    app.pabIsPressed = False



def timerFired(app):
    if app.startingMenu:

        if app.time == 0:
            createOneGreenPlatform(app)

        app.time += 0.5
        if app.time % 1000 == 0:
            app.gameSeconds += 1
        if app.time > 8.1:
            app.time = 8.1
        # Gravity is always affecting the character 
        (app.startingDoodle.cy, app.startingDoodle.yv) = Gravity.falling(app.startingDoodle.cy, app.startingDoodle.yv, app.a, app.time)

        # collision gives boost in negative velocity 
        if (Collisions.isCollision(app.startingDoodle.cx, app.startingDoodle.cy,
            app.hitboxes) and app.startingDoodle.yv > 0 ):
            app.startingDoodle.yv = Gravity.jump()
        if (Collisions.isCollision(app.startingDoodle.cx, app.startingDoodle.cy, 
            app.blueHitboxes) and app.startingDoodle.yv > 0 ):
            app.startingDoodle.yv = Gravity.jump()


    if app.playingGame and app.stopGravity == False:
        if app.time == 8.1:
            app.time = 0
            app.platforms.pop()
            app.hitboxes.pop()
        

        # Gravity is always affecting the character 
        (app.player.cy, app.player.yv) = Gravity.falling(app.player.cy, app.player.yv, app.a, app.time)
        (app.player.cx) += app.player.xv*app.time

        if app.gameOver != True:

            if app.dazed != True:
                # collision gives boost in negative velocity 
                if Collisions.isCollision(app.player.cx, app.player.cy, app.hitboxes) and app.player.yv > 0:
                    app.player.yv = Gravity.jump()
                if Collisions.isCollision(app.player.cx, app.player.cy, app.blueHitboxes) and app.player.yv > 0:
                    app.player.yv = Gravity.jump() 
                
            if enemyCollisions(app):
                app.doodle = app.normaldoodle
                app.dazed = True
                app.player.yv = 0
                
            if app.dazed:
                loopStars(app)

            # difficulty
            if 1500 < app.score < 2000 and app.max_green_y_distance < 150:
                app.max_green_y_distance += 10
            
            if 2500 < app.score and app.max_green_y_distance < 200:
                app.max_green_y_distance += 1


            if app.player.yv < 0:
                app.score += round(abs(app.player.yv)*app.time)
                # jumping down helps reduce the value 
            
            spawnPlatforms_and_Hitboxes(app)
            spawnBlueMonster(app)

            app.waveTime += 0.8
            app.time += 1
            if app.time % 1000 == 0:
                app.gameSeconds += 1
            if app.time > 8:
                app.time = 8

            moveBluePlatforms(app)
            moveGreenPlatforms(app)
            
            
            monsterMovement(app)


            # so it doesn't seem like he jumps 2x the height
            if app.player.cy < 450:
                app.player.cy = 450
            
            # wrap around 
            if app.player.cx < -20:
                app.player.cx = 600
            elif app.player.cx > 620:
                app.player.cx = 0

            # update bullet
            for bullet in app.bullets:
                bullet[1] -= (8)*app.time
                if bullet[1] < 0:
                    app.bullets.remove(bullet)
                
    
            if app.player.cy > 1000:
                app.gameOver = True
        
        if app.gameOver:
            if app.player.cy > 1000 and len(app.platforms) > 0:
                app.player.yv = -4
            moveGreenPlatformsUp(app)
            if app.gameOverY > 400:
                moveGameOverScreenUp(app)
            if app.player.cy > 1200 and len(app.platforms) == 0:
                app.stopGravity = True
                app.playingGame = False
            loopStars(app)
        
    if len(app.bullets) > 0:
        app.doodle = app.shooter

    


def keyPressed(app, event):
    if app.playingGame and app.gameOver != True and app.dazed != True: 
        if event.key == 'a':
            app.player.xVel(-1.5)
            if app.player.xv < 0 and len(app.bullets) == 0:
                    app.doodle = app.normaldoodle
        elif event.key == 'd':
            app.player.xVel(1.5)
            if app.player.xv > 0 and len(app.bullets) == 0:
                app.doodle = app.rightDoodle
        elif event.key == "Space":
            app.bullets.append([app.player.cx, app.player.cy])

def keyReleased(app, event):
    if app.playingGame and app.gameOver != True: 
        if event.key == 'a':
            app.player.xVel(0)
        elif event.key == 'd':
            app.player.xVel(0)
        

def drawDoodle(app, canvas):
    canvas.create_image(app.player.cx, app.player.cy, image=ImageTk.PhotoImage(app.doodle))

def drawBullet(app, canvas):
    for bullet in app.bullets:
        cx, cy = bullet[0], bullet[1]
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.bullet))

def spawnPlatforms_and_Hitboxes(app):
    if app.time == 0:
        L = [[300, 900]]
        initialPlatforms = 15
        initialMaxDistance = 150
        startingMap = Platform.createInitialMap(L, initialPlatforms, initialMaxDistance)
        for platform in startingMap:
            app.platforms.append(platform)
            lx, ly, rx, ry = Platform.createHitbox(platform[0], platform[1])
            app.hitboxes.append([lx, ly, rx, ry])

    # keeps spawning platforms above playable area 
    if Platform.needsMorePlatforms(app.platforms):
        L = []
        nextLevels = Platform.infiniteSpawner(L, app.num_green_platforms, app.max_green_y_distance)
        for platform in nextLevels:
            app.platforms.append(platform)
            lx, ly, rx, ry = Platform.createHitbox(platform[0], platform[1])
            app.hitboxes.append([lx, ly, rx, ry])
          
    if app.gameSeconds % 5 == 0:
        if len(app.bluePlatforms) < 1:
            bcx, bcy = Platform.basicSpawn(200, 400, -75, -5)
            blx, bly, brx, bry = Platform.createHitbox(bcx, bcy)
            app.bluePlatforms.append([bcx, bcy])
            app.blueHitboxes.append([blx, bly, brx, bry])

def drawBackground(app, canvas):
    canvas.create_image(300, 500, image=ImageTk.PhotoImage(app.background))

def drawPlatform(app, canvas):
    for platform in app.platforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.platform))

def moveGreenPlatforms(app):
    # moves the platforms and their hitboxes nicely
    for platform in app.platforms:
        if app.player.cy < 450:
            if app.player.yv < 0:
                platform[1] += abs(app.player.yv)*app.time            
        if platform[1] > 1000:
            app.platforms.remove(platform)
    for hitbox in app.hitboxes:
        if app.player.cy < 450:
            if app.player.yv < 0:
                hitbox[1] += abs(app.player.yv)*app.time
                hitbox[3] += abs(app.player.yv)*app.time
        if hitbox[1] > 1000:
            app.hitboxes.remove(hitbox)

# high score is making a text file and saving the scores there and it reads it from there every time 

def drawBluePlatform(app, canvas):
    for platform in app.bluePlatforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.bluePlatform))

def moveBluePlatforms(app):
    # makes blue platforms move side to side and up and down
    for platform in app.bluePlatforms:
        if app.player.cy < 450:
            if app.player.yv < 0:
                platform[1] += abs(app.player.yv)*app.time  
        platform[0] += app.bluedx
        if platform[0] > 557.5 or platform[0] < 65:
            app.bluedx *= -1
        if platform[1] > 1000:
            app.bluePlatforms.remove(platform)
    # vertical part 
    for hitbox in app.blueHitboxes:
        if app.player.cy < 450:
            if app.player.yv < 0:
                hitbox[1] += abs(app.player.yv)*app.time
                hitbox[3] += abs(app.player.yv)*app.time    
        hitbox[0] += app.bluedx
        hitbox[2] += app.bluedx
        if hitbox[0] > 642.5 or hitbox[2] < -65:
            app.bluedx *= -1
        if hitbox[1] > 1000:
            app.blueHitboxes.remove(hitbox)

def spawnBlueMonster(app):
    if app.gameSeconds % 5 == 0 and len(app.monsterList) < 1:
        cx, cy = Monster.spawnEnemy()
        return app.monsterList.append(Monster(cx, cy)) 

def monsterMovement(app):
    for monster in app.monsterList:
        if monster.cy > 1000:
            app.monsterList.remove(monster)
        if app.player.cy < 450:
            if app.player.yv < 0:
                monster.cy += abs(app.player.yv)*app.time
        monster.cy += 5*math.sin(app.waveTime)
        monster.cx += app.monsterdx
        if monster.cx > 570 or monster.cx < 30:
            app.monsterdx *= -1
            app.blueMonster = app.blueMonster.transpose(Image.FLIP_LEFT_RIGHT)
        lx, rx, ty, by = Monster.enemyHitbox(monster.cx, monster.cy)
        for bullet in app.bullets:
            if lx <= bullet[0] <= rx and ty <= bullet[1] <= by:
                app.bullets.remove(bullet)
                app.monsterList.pop()


def drawBlueMonster(app, canvas):
    for monster in app.monsterList:
        canvas.create_image(monster.cx, monster.cy, 
                    image=ImageTk.PhotoImage(app.blueMonster))

def enemyCollisions(app):
    for monster in app.monsterList:
        xDistance = abs(app.player.cx - monster.cx)
        yDistance = abs(app.player.cy - monster.cy)
        if xDistance <= (20 + 30) and yDistance <= (40 + 30): # distance from middle to side or top/bot
            return True
    return False
        

def loopStars(app):
    app.dazedIndex += 1
    if app.dazedIndex > 2:
        app.dazedIndex = 0
    if app.dazedIndex < 3:
        app.dazedImg = app.dazedList[app.dazedIndex]

def drawStars(app, canvas):
    if app.dazed:
        canvas.create_image(app.player.cx+10, app.player.cy-30, image=ImageTk.PhotoImage(app.dazedImg))


# For starting menu 
def drawStartingDoodle(app, canvas):
    canvas.create_image(app.startingDoodle.cx, app.startingDoodle.cy, 
                                image=ImageTk.PhotoImage(app.doodle))

def createOneGreenPlatform(app):
    app.platforms.append([160, 800])
    lx, ly, rx, ry = Platform.createHitbox(150, 800)
    app.hitboxes.append([lx, ly, rx, ry])

def drawTitle(app, canvas):
    canvas.create_image(250, 300, image=ImageTk.PhotoImage(app.title))

def drawPlayButton(app, canvas):
    canvas.create_image(app.playButtonButton.cx, app.playButtonButton.cy, 
                                image=ImageTk.PhotoImage(app.playButton))

def drawPbIsPressed(app, canvas):
    if app.pbIsPressed == True:
        canvas.create_image(app.playButtonButton.cx, app.playButtonButton.cy, 
                                    image=ImageTk.PhotoImage(app.pressedPB))


# for game over screen 
def drawGameOverScreen(app, canvas):
    canvas.create_text(app.gameOverX, app.gameOverY-50, 
                    text = "Game Over!", font = ("Comic Sans MS", 30))
    canvas.create_text(app.gameOverX, app.gameOverY+50, 
                text= f"Your Score: {app.score}", font = ("Comic Sans MS", 20))
    

def moveGreenPlatformsUp(app):
    for platform in app.platforms:
        platform[1] -= abs(app.player.yv)*app.time            
        if platform[1] < 0:
            app.platforms.remove(platform)
    for hitbox in app.hitboxes:
        hitbox[1] -= abs(app.player.yv)*app.time
        hitbox[3] -= abs(app.player.yv)*app.time
        if hitbox[1] < 0:
            app.hitboxes.remove(hitbox)

def moveGameOverScreenUp(app):
    app.gameOverY -= abs(app.player.yv)*app.time
    app.playAgainButton.cy -= abs(app.player.yv)*app.time

def drawPlayAgainButton(app, canvas):
    canvas.create_image(app.playAgainButton.cx, app.playAgainButton.cy, 
                                image=ImageTk.PhotoImage(app.playAgain))
def drawPaButtonIsPressed(app, canvas):
    if app.pabIsPressed == True:
        canvas.create_image(app.playAgainButton.cx, app.playAgainButton.cy, 
                                    image=ImageTk.PhotoImage(app.playAgainOn))
def mousePressed(app, event):
    lx, rx, ty, by = app.playButtonButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.pbIsPressed = True
    lx, rx, ty, by = app.playAgainButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.pabIsPressed = True

def mouseReleased(app, event):
    lx, rx, ty, by = app.playButtonButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.startingMenu = False
        app.playingGame = True
    app.pbIsPressed = False
    lx, rx, ty, by = app.playAgainButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        appStarted(app)
    app.pabIsPressed = False


def redrawAll(app, canvas):
    drawBackground(app, canvas)

    if app.startingMenu:
        drawStartingDoodle(app, canvas)
        drawPlatform(app, canvas)
        drawTitle(app, canvas)
        drawPlayButton(app, canvas)
        drawPbIsPressed(app, canvas)

    if app.playingGame and app.gameOver != True:
        drawPlatform(app, canvas)
        drawBluePlatform(app, canvas)
        drawBlueMonster(app, canvas)
        drawBullet(app, canvas)
        drawDoodle(app, canvas)  
        drawStars(app, canvas)
        canvas.create_rectangle(0, 0, 600, 50, fill = "burlywood1", outline = "burlywood1")
        canvas.create_text(60, 25, 
        text= f"{app.score}", font = ("Comic Sans MS", 18))

    if app.gameOver:
        drawPlatform(app, canvas)
        drawDoodle(app, canvas)
        drawStars(app, canvas)
        drawGameOverScreen(app, canvas)
        drawPlayAgainButton(app, canvas)
        drawPaButtonIsPressed(app, canvas)


runApp(width = 600, height = 1000)


