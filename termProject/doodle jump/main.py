''' 
Main file: Runs all classes and game

'''

#imports
from cmu_112_graphics import *
import math

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

    app.player = Player(300, 400, 0, 0)

    app.a = 0.01
    app.time = 0
    app.gameSeconds = 0
    
    app.platforms = []
    app.hitboxes = []
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

def drawBullet(app, canvas, cx, cy):
    r = 5
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


def drawPlatform(app, canvas):
    for platform in app.platforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.platform))


def redrawAll(app, canvas):
    drawPlatform(app, canvas)
    drawDoodle(app, canvas)
    for bullet in app.bullets:
        cx, cy = bullet
        drawBullet(app, canvas, cx, cy)
    canvas.create_text(300, 100, 
    text= f"""
    xPos = {app.player.cx}, yPos = {app.player.cy} 
        yv = {app.player.yv}, xv = {app.player.xv}""")

runApp(width = 600, height = 1000)


