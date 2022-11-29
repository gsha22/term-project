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


def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")
    app.normaldoodle = app.scaleImage(app.doodle, 2/3)
    app.doodle = app.normaldoodle

    app.shooter = app.loadImage("shooting_doodle.png")
    app.shooter = app.scaleImage(app.shooter, 6/5)

    app.platform = app.loadImage("green_platform.png")
    app.platform = app.scaleImage(app.platform, 2/3)
    app.num_green_platforms = 5
    app.max_green_y_distance = 100

    app.bluePlatform = app.loadImage("blue_platform.png")
    app.bluePlatform = app.scaleImage(app.bluePlatform, 2/3)
    app.bluedx = 3

    #BACKGROUND
    app.background = app.loadImage("background.png")
    app.background = app.scaleImage(app.background, 4/3)

    app.player = Player(300, 400, 0, 0)

    app.a = 0.01
    app.time = 0
    app.gameSeconds = 0
    
    app.platforms = []
    app.hitboxes = []

    app.bluePlatforms = []
    app.blueHitboxes = []

    app.bullets = []

    app.timerDelay = 1

    app.score = 0

    # Starting Menu
    app.startingMenu = True
    app.startingDoodle = Player(150, 600, 0, 0)

    #currently playing the game
    app.playingGame = False

    # Game Over
    app.gameOver = False

    

def timerFired(app):

    if app.startingMenu:

        if app.time == 0:
            createOneGreenPlatform(app)

        app.time += 0.5
        if app.time % 1000 == 0:
            app.gameSeconds += 1
        if app.time > 8:
            app.time = 8
        # Gravity is always affecting the character 
        (app.startingDoodle.cy, app.startingDoodle.yv) = Gravity.falling(app.startingDoodle.cy, app.startingDoodle.yv, app.a, app.time)

        # collision gives boost in negative velocity 
        if Collisions.isCollision(app.startingDoodle.cx, app.startingDoodle.cy, app.hitboxes) and app.startingDoodle.yv > 0:
            app.startingDoodle.yv = Gravity.jump()
        if Collisions.isCollision(app.startingDoodle.cx, app.startingDoodle.cy, app.blueHitboxes) and app.startingDoodle.yv > 0:
            app.startingDoodle.yv = Gravity.jump() 


    if app.playingGame:

        # app.platforms.pop()
        # app.hitboxes.pop()
        # Gravity is always affecting the character 
        (app.player.cy, app.player.yv) = Gravity.falling(app.player.cy, app.player.yv, app.a, app.time)

        # collision gives boost in negative velocity 
        if Collisions.isCollision(app.player.cx, app.player.cy, app.hitboxes) and app.player.yv > 0:
            app.player.yv = Gravity.jump()
        if Collisions.isCollision(app.player.cx, app.player.cy, app.blueHitboxes) and app.player.yv > 0:
            app.player.yv = Gravity.jump() 

        # difficulty
        if 1500 < app.score < 2000 and app.max_green_y_distance < 150:
            app.max_green_y_distance += 10
        
        if 2500 < app.score and app.max_green_y_distance < 200:
            app.max_green_y_distance += 1


        if app.player.yv < 0:
            app.score += round(abs(app.player.yv)*app.time)
        
        spawnPlatforms_and_Hitboxes(app)

        app.time += 1
        if app.time % 1000 == 0:
            app.gameSeconds += 1
        if app.time > 8:
            app.time = 8

        
        # makes blue platforms move side to side and up and down
        for platform in app.bluePlatforms:
            if app.player.cy < 450:
                if app.player.yv < 0:
                    platform[1] += abs(app.player.yv)*app.time  
            
            # blue platforms don't bounce back yet idk why
            
            platform[0] += app.bluedx
            if platform[0] > 557.5 or platform[0] < 65:
                app.bluedx *= -1

            if platform[1] > 1000:
                app.bluePlatforms.remove(platform)
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
            bullet[1] -= (2)*app.time
            if bullet[1] < 0:
                app.bullets.remove(bullet)
    
        
def keyPressed(app, event):
    if app.playingGame: 
        if event.key == "a":
            if app.player.xv > 0:
                app.doodle = app.doodle.transpose(Image.FLIP_LEFT_RIGHT)
            app.player.xMovements(-4, app.time)
        elif event.key == "d":
            if app.player.xv <= 0:
                app.doodle = app.doodle.transpose(Image.FLIP_LEFT_RIGHT)
            app.player.xMovements(4, app.time)
        elif event.key == "Space":
            # app.doodle = app.shooter
            app.bullets.append([app.player.cx, app.player.cy])
        

def drawDoodle(app, canvas):
    canvas.create_image(app.player.cx, app.player.cy, image=ImageTk.PhotoImage(app.doodle))

def drawBullet(app, canvas):
    r = 5
    for bullet in app.bullets:
        cx, cy = bullet
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'red')

def spawnPlatforms_and_Hitboxes(app):
    if app.time == 0:
        L = [[300, 900]]
        initialPlatforms = 15
        initialMaxDistance = 100
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

def drawBluePlatform(app, canvas):
    for platform in app.bluePlatforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.bluePlatform))

# For starting menu 
def drawStartingDoodle(app, canvas):
    canvas.create_image(app.startingDoodle.cx, app.startingDoodle.cy, image=ImageTk.PhotoImage(app.doodle))

def createOneGreenPlatform(app):
    app.platforms.append([160, 800])
    lx, ly, rx, ry = Platform.createHitbox(150, 800)
    app.hitboxes.append([lx, ly, rx, ry])

def redrawAll(app, canvas):
    drawBackground(app, canvas)

    if app.startingMenu:
        drawStartingDoodle(app, canvas)
        drawPlatform(app, canvas)

    if app.playingGame:
        drawPlatform(app, canvas)
        drawBluePlatform(app, canvas)
        drawDoodle(app, canvas)    
        drawBullet(app, canvas)
        canvas.create_rectangle(0, 0, 600, 50, fill = "burlywood1", outline = "burlywood1")
        canvas.create_text(60, 25, 
        text= f"{app.score}", font = ("Comic Sans MS", 18))



runApp(width = 600, height = 1000)


