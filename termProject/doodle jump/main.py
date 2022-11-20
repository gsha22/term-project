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

from PIL import Image

def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")
    app.normaldoodle = app.scaleImage(app.doodle, 2/3)
    app.doodle = app.normaldoodle

    app.shooter = app.loadImage("shooting_doodle.png")
    app.shooter = app.scaleImage(app.shooter, 6/5)

    app.platform = app.loadImage("green_platform.png")
    app.platform = app.scaleImage(app.platform, 2/3)

    app.bluePlatform = app.loadImage("blue_platform.png")
    app.bluePlatform = app.scaleImage(app.bluePlatform, 2/3)

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

    

def timerFired(app):
    
    spawnPlatforms_and_Hitboxes(app)

    app.time += 1
    if app.time % 1000 == 0:
        app.gameSeconds += 1
    if app.time > 8:
        app.time = 8

    # Gravity is always affecting the character 
    (app.player.cy, app.player.yv) = Gravity.falling(app.player.cy, app.player.yv, app.a, app.time)

    # collision gives boost in negative velocity 
    if Collisions.isCollision(app.player.cx, app.player.cy, app.hitboxes) and app.player.yv > 0:
        app.player.yv = Gravity.jump()
    if Collisions.isCollision(app.player.cx, app.player.cy, app.blueHitboxes) and app.player.yv > 0:
        app.player.yv = Gravity.jump() 
    
    # makes blue platforms move side to side and up and down
    for platform in app.bluePlatforms:
        if app.player.cy < 450:
            if app.player.yv < 0:
                platform[1] += abs(app.player.yv)*app.time  
        
        # blue platforms don't bounce back yet 
        dx = 1
        platform[0] += dx
        if platform[0] > 600 or platform[0] < 0:
            dx *= -1

        if platform[1] > 1000:
            app.bluePlatforms.remove(platform)
    for hitbox in app.blueHitboxes:
        if app.player.cy < 450:
            if app.player.yv < 0:
                hitbox[1] += abs(app.player.yv)*app.time
                hitbox[3] += abs(app.player.yv)*app.time
        
        # blue platforms don't bounce back yet 
        dx = 1
        hitbox[0] += dx
        hitbox[2] += dx

        if hitbox[0] > 642.5 or hitbox[2] < -65:
            dx *= -1

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
    
        
def keyPressed(app, event):
    if event.key == "a":
        if app.player.xv > 0:
            app.doodle = app.doodle.transpose(Image.FLIP_LEFT_RIGHT)
        app.player.xMovements(-2, app.time)
    elif event.key == "d":
        if app.player.xv <= 0:
            app.doodle = app.doodle.transpose(Image.FLIP_LEFT_RIGHT)
        app.player.xMovements(2, app.time)
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
        for x in range(18):
            cx, cy = Platform.spawn(50, 550, 100, 900)
            lx, ly, rx, ry = Platform.createHitbox(cx, cy)
            # if Platform.isLegalPlatform(cx, cy, app.platforms):
            app.platforms.append([cx, cy])
            app.hitboxes.append([lx, ly, rx, ry])
    
    # keeps spawning platforms above playable area 
    if len(app.platforms) < 20:
        cx, cy = Platform.spawn(50, 550, -75, -5)
        lx, ly, rx, ry = Platform.createHitbox(cx, cy)
        if Platform.isLegalPlatform(cx, cy, app.platforms):
            app.platforms.append([cx, cy])
            app.hitboxes.append([lx, ly, rx, ry])
            
    if app.gameSeconds % 5 == 0:
        if len(app.bluePlatforms) < 2:
            bcx, bcy = Platform.spawn(200, 400, -75, -5)
            blx, bly, brx, bry = Platform.createHitbox(bcx, bcy)
            app.bluePlatforms.append([bcx, bcy])
            app.blueHitboxes.append([blx, bly, brx, bry])


def drawPlatform(app, canvas):
    for platform in app.platforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.platform))

def drawBluePlatform(app, canvas):
    for platform in app.bluePlatforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.bluePlatform))

def redrawAll(app, canvas):
    drawPlatform(app, canvas)
    drawBluePlatform(app, canvas)
    drawDoodle(app, canvas)    
    drawBullet(app, canvas)
    canvas.create_text(300, 100, 
    text= f"""
    xPos = {app.player.cx}, yPos = {app.player.cy} 
        yv = {app.player.yv}, xv = {app.player.xv}""")

runApp(width = 600, height = 1000)


