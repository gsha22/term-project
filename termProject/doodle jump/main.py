''' 
Main file: Runs all classes and game

'''

#imports
from cmu_112_graphics import *
import math

from Physics import Gravity

def appStarted(app): 
    # SPRITES:
    app.doodle = app.loadImage("doodle.png")

    app.doodleX = 300
    app.doodleY = 400
    app.doodleV = 0
    app.a = 6
    app.time = 0
    app.seconds = 0
    app.player = [app.doodleY, app.doodleV, app.a, app.time]

# hello

def timerFired(app):
    app.time += 1
    # if app.time % 10 == 0:
    #     app.seconds += 1
    (y, v, a) = Gravity.falling(app.doodleY, app.doodleV, app.a, app.time)
    app.doodleY = y
    app.doodleV = v
    app.a = a
        

def mousePressed(app, event):
    app.doodleX = event.x
    app.doodleY = event.y
    app.doodleV = 0
    app.time = 0

def drawDoodle(app, canvas):
    canvas.create_image(app.doodleX, app.doodleY, image=ImageTk.PhotoImage(app.doodle))


def drawPlatform(app, canvas):
    canvas.create_rectangle(100, 950, 500, 1000, fill = 'black')
    pass


def redrawAll(app, canvas):
    drawDoodle(app, canvas)
    drawPlatform(app, canvas)
    canvas.create_text(300, 100, text=f"yPos = {app.doodleY}\n v = {app.doodleV}")

runApp(width = 600, height = 1000)


