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

def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")
    app.doodle = app.scaleImage(app.doodle, 2/3)

    app.platform = app.loadImage("green_platform.png")
    app.platform = app.scaleImage(app.platform, 2/3)

    # app.doodleX = 300
    # app.doodleY = 400
    # app.doodleV = 0

    app.player = Player(300, 400, 0, 0)

    app.a = 0.01
    app.time = 0
    app.gameSeconds = 0
    
    app.platforms = []
    app.hitboxes = []

    app.timerDelay = 1

def timerFired(app):
    
    if app.time == 0: spawnPlatforms_and_Hitboxes(app)
    app.time += 1
    if app.time % 1000 == 0:
        app.gameSeconds += 1
    if app.time > 8:
        app.time = 8
    (app.player.cy, app.player.yv, a) = Gravity.falling(app.player.cy, app.player.yv, app.a, app.time)

    if Collisions.isCollision(app.player.cx, app.player.cy, app.hitboxes) and app.player.yv > 0:
        app.player.yv = Gravity.jump()
    
    for platform in app.platforms:
        if app.player.cy < 450:
            platform[1] += 2
        if platform[1] > 1000:
            app.platforms.remove(platform)
    for hitbox in app.hitboxes:
        if app.player.cy < 450:
            hitbox[1] += 2
            hitbox[3] += 2
        if hitbox[1] > 1000:
            app.hitboxes.remove(hitbox)
        
        
def keyPressed(app, event):
    if event.key == "a":
        app.player.xMovements(-15)
    elif event.key == "d":
        app.player.xMovements(15)


def drawDoodle(app, canvas):
    canvas.create_image(app.player.cx, app.player.cy, image=ImageTk.PhotoImage(app.doodle))


def spawnPlatforms_and_Hitboxes(app):
    for x in range(20):
        cx, cy = Platform.spawn()
        lx, ly, rx, ry = Platform.createHitbox(cx, cy)
        app.platforms.append([cx, cy])
        app.hitboxes.append([lx, ly, rx, ry])

def drawPlatform(app, canvas):
    for platform in app.platforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.platform))


def redrawAll(app, canvas):
    drawPlatform(app, canvas)
    drawDoodle(app, canvas)
    canvas.create_text(300, 100, 
    text= f"""xPos = {app.player.cx}, yPos = {app.player.cy} 
            v = {app.player.yv}, t = {app.time}""")

runApp(width = 600, height = 1000)


