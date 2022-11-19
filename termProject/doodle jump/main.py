''' 
Main file: Runs all classes and game

'''

#imports
from cmu_112_graphics import *
import math

from Physics import Gravity
from Physics import Collisions

from Platforms import Platform

def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")
    app.doodle = app.scaleImage(app.doodle, 2/3)

    app.platform = app.loadImage("green_platform.png")
    app.platform = app.scaleImage(app.platform, 2/3)

    app.doodleX = 300
    app.doodleY = 400
    app.doodleV = 0
    app.a = 6
    app.time = 0
    app.seconds = 0
    
    app.platforms = []
    app.hitboxes = []


def timerFired(app):
    if app.time == 0: spawnPlatforms_and_Hitboxes(app)
    app.time += 1
    # if app.time % 10 == 0:
    #     app.seconds += 1
    (y, v, a) = Gravity.falling(app.doodleY, app.doodleV, app.a, app.time)
    # if len(app.hitboxes) > 0:
        # (v, t) = Collisions.collide(app.doodleX, app.doodleY, app.doodleV, app.time, app.hitboxes)
    app.doodleY = y
    app.doodleV = v
    app.a = a
    # app.t = t
        

# def mousePressed(app, event):
#     app.doodleX = event.x
#     app.doodleY = event.y
#     app.doodleV = 0
#     app.time = 0


def keyPressed(app, event):
    if event.key == "a":
        app.doodleX -= 5
    elif event.key == "d":
        app.doodleX += 5


def drawDoodle(app, canvas):
    canvas.create_image(app.doodleX, app.doodleY, image=ImageTk.PhotoImage(app.doodle))


def spawnPlatforms_and_Hitboxes(app):
    cx, cy = Platform.spawn()
    lx, ly, rx, ry = Platform.createHitbox(cx, cy)
    app.platforms.append([cx, cy])
    app.hitboxes.append([lx, ly, rx, ry])

def drawPlatform(app, canvas):
    for platform in app.platforms:
        cx, cy = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.platform))


def redrawAll(app, canvas):
    drawDoodle(app, canvas)
    drawPlatform(app, canvas)
    canvas.create_text(300, 100, text=f"xPos = {app.doodleX}, yPos = {app.doodleY}\n v = {app.doodleV}")

runApp(width = 600, height = 1000)


