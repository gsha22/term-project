''' 
Main file: Runs all classes and game
'''

'''

Welcome to 112 Jump!! 

If you didn't see the readme directions, the controls are "a" and "d" to move
side to side, and then space bar to shoot. The goal is to keep jumping as high
as possible! If you collide with the enemies, you will become dazed and fall off. 

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
from Button import RectangleButton
from Enemy import Monster

import pygame

# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
import ast

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)


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


    app.spring = app.loadImage("spring.png")
    app.spring = app.scaleImage(app.spring, 2/3)
    app.extendedSpring = app.loadImage("spring_extended.png")
    app.extendedSpring = app.scaleImage(app.extendedSpring, 2/3)
    app.springImg = app.spring

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
    app.springs = []

    app.timerDelay = 1

    app.score = 0
    app.difficulty = False

    app.mouseX = 0
    app.mouseY = 0

    app.movement = set()

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

    app.gameOverTitle = app.loadImage("game_over.png")
    app.playerName = 'Doodler'
    app.ncbX = 400
    app.ncbY = 1590
    app.nameChangeButton = RectangleButton(app.ncbX, app.ncbY)
    app.changeName = False

    app.ttc = app.loadImage("tap_to_change.png")

    # scoreboard 
    app.scoreboard = ast.literal_eval(readFile('scoreboard.txt'))
    
    app.trophy = app.loadImage("scorescup.png")
    app.trophyOn = app.loadImage("scorescup_on.png")
    app.trophyButton = RectangleButton(450, 700)

    app.trophyPressed = False

    # leaderboard screen
    app.leaderboard = False

    app.menuButton = CircleButton(300, 900)
    app.menu = app.loadImage("menu.png")
    app.menu = app.scaleImage(app.menu, 2/3)

    app.menuOn = app.loadImage("menu-on.png")
    app.menuOn = app.scaleImage(app.menuOn, 2/3)

    app.menuIsPressed = False

    # sounds 
    pygame.mixer.init()
    app.jump = pygame.mixer.Sound("jump.wav")
    app.shoot = pygame.mixer.Sound("pistol_shoot.mp3")
    app.boing = pygame.mixer.Sound("boing.mp3")

    # HARD once you get to 50K meters!! 
    app.hardMode = False
    app.easyMode = True



def timerFired(app):
    if app.startingMenu:

        if app.time == 0:
            createOneGreenPlatform(app)
            app.difficulty = False

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
            pygame.mixer.Sound.play(app.jump)
        if (Collisions.isCollision(app.startingDoodle.cx, app.startingDoodle.cy, 
            app.blueHitboxes) and app.startingDoodle.yv > 0 ):
            app.startingDoodle.yv = Gravity.jump()
            pygame.mixer.Sound.play(app.jump)


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
                    pygame.mixer.Sound.play(app.jump)
                if Collisions.isCollision(app.player.cx, app.player.cy, app.blueHitboxes) and app.player.yv > 0:
                    app.player.yv = Gravity.jump() 
                    pygame.mixer.Sound.play(app.jump)
                
            if enemyCollisions(app):
                app.dazed = True
                app.player.yv = 0
                
            if app.dazed:
                loopStars(app)
                app.doodle = app.normaldoodle
            
            xDirectionMovement(app)
                

            # difficulty
            if 1500 < app.score < 2000 and app.max_green_y_distance < 150:
                app.max_green_y_distance += 10
            
            if 2500 < app.score and app.max_green_y_distance < 200:
                app.max_green_y_distance += 1
            
            if app.score > 4500:
                app.difficulty = True
            
            if app.score > 20000:
                app.easyMode = False
                app.hardMode = True

            if app.player.cy < 450:
                if app.player.yv < 0:
                    app.score += round(abs(app.player.yv)*app.time)
                
            
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

            spawnSpring(app)
            moveSpring(app)

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

    
def xDirectionMovement(app):
    if 'a' in app.movement:
        if app.player.xVel != -1.5:
            app.player.xVel(-1.5)
            if app.player.xv < 0 and len(app.bullets) == 0:
                    app.doodle = app.normaldoodle
    elif 'd' in app.movement:
        if app.player.xVel != 1.5:
            app.player.xVel(1.5)
            if app.player.xv > 0 and len(app.bullets) == 0:
                app.doodle = app.rightDoodle

def keyPressed(app, event):
    if app.playingGame and app.gameOver != True and app.dazed != True: 
        if 'a' not in app.movement and event.key == 'a':
            app.movement.add('a')
        elif 'd' not in app.movement and event.key == 'd':
            app.movement.add('d')
        elif event.key == "Space":
            pygame.mixer.Sound.play(app.shoot)
            app.bullets.append([app.player.cx, app.player.cy])

def keyReleased(app, event):
    if app.playingGame and app.gameOver != True: 
        if 'a' in app.movement and event.key == 'a':
            app.movement.remove('a')
            app.player.xVel(0)
        elif 'd' in app.movement and event.key == 'd':
            app.movement.remove('d')
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
    if app.easyMode:
        if Platform.needsMorePlatforms(app.platforms):
            L = []
            nextLevels = Platform.infiniteSpawner(L, app.num_green_platforms, app.max_green_y_distance, app.difficulty)
            for platform in nextLevels:
                    app.platforms.append(platform)
                    lx, ly, rx, ry = Platform.createHitbox(platform[0], platform[1])
                    app.hitboxes.append([lx, ly, rx, ry])
        if app.gameSeconds % 5 == 0:
            if len(app.bluePlatforms) < 1:
                bcx, bcy = Platform.basicSpawn(200, 400, -75, -5)
                blx, bly, brx, bry = Platform.createHitbox(bcx, bcy)
                dx = 2
                app.bluePlatforms.append([bcx, bcy, dx])
                app.blueHitboxes.append([blx, bly, brx, bry, dx])

    if app.hardMode: 
        if Platform.needsMorePlatforms(app.bluePlatforms):
            L = []
            nextLevels = Platform.infiniteSpawner(L, app.num_green_platforms, app.max_green_y_distance, app.difficulty)
            for platform in nextLevels:
                platform += [2]
                app.bluePlatforms.append(platform)
                dx = 2
                blx, bly, brx, bry = Platform.createHitbox(platform[0], platform[1])
                app.blueHitboxes.append([blx, bly, brx, bry, dx])
        if app.gameSeconds % 5 == 0:
            if len(app.platforms) < 1:
                cx, cy = Platform.basicSpawn(200, 400, -75, -5)
                lx, ly, rx, ry = Platform.createHitbox(cx, cy)
                app.platforms.append([cx, cy])
                app.hitboxes.append([lx, ly, rx, ry])

def spawnSpring(app):
    if app.easyMode:
        if len(app.springs) < 1 and app.gameSeconds % 5 == 0:
            app.springImg = app.spring
            platformNum = random.randint(0, len(app.platforms)-1)
            pcx, pcy = app.platforms[platformNum] 
            if pcy < 0:
                # plx, ply, prx, pby = Platform.createHitbox(pcx, pcy)
                # print(plx, prx)
                scx = pcx - 20
                scy = pcy - 40
                app.springs.append([scx, scy])


def moveSpring(app):
    for spring in app.springs:
        if app.player.cy < 450:
            if app.player.yv < 0:
                spring[1] += abs(app.player.yv)*app.time            
        if spring[1] > 1000:
            app.springs.remove(spring) 
        lx, rx, ty, by = Player.playerHitbox(app.player.cx, app.player.cy)
        if lx < spring[0] < rx and ty < spring[1] - 5 < by and app.player.yv > 0:
            if app.dazed != True:
                app.player.yv = -4
                app.springImg = app.extendedSpring
                pygame.mixer.Sound.play(app.boing)

# def drawPlayerHitbox(app, canvas):
#     lx, rx, ty, by = Player.playerHitbox(app.player.cx, app.player.cy)
#     canvas.create_rectangle(lx, ty, rx, by)

def drawSpring(app, canvas):
    for spring in app.springs:
        cx, cy = spring[0], spring[1]
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.springImg))

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


def drawBluePlatform(app, canvas):
    for platform in app.bluePlatforms:
        cx, cy, dx = platform
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.bluePlatform))

def moveBluePlatforms(app):
    # makes blue platforms move side to side and up and down
    for platform in app.bluePlatforms:
        if app.player.cy < 450:
            if app.player.yv < 0:
                platform[1] += abs(app.player.yv)*app.time  
        platform[0] += platform[2]
        if platform[0] > 557.5 or platform[0] < 65:
            platform[2] *= -1
        if platform[1] > 1000:
            app.bluePlatforms.remove(platform)
    # vertical part 
    for hitbox in app.blueHitboxes:
        if app.player.cy < 450:
            if app.player.yv < 0:
                hitbox[1] += abs(app.player.yv)*app.time
                hitbox[3] += abs(app.player.yv)*app.time    
        hitbox[0] += hitbox[4]
        hitbox[2] += hitbox[4]
        if hitbox[2] > 600 or hitbox[0] < 0:
            hitbox[4] *= -1
        if hitbox[1] > 1000:
            app.blueHitboxes.remove(hitbox)

def drawBlueHitboxes(app, canvas):
    for hitbox in app.blueHitboxes:
        lx, ly, rx, ry, dx = hitbox
        canvas.create_rectangle(lx, ly, rx, ry)

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

def drawTrophy(app, canvas):
    canvas.create_image(app.trophyButton.cx, app.trophyButton.cy, image=ImageTk.PhotoImage(app.trophy))

def drawTrophyOn(app, canvas):
    if app.trophyPressed:
        canvas.create_image(app.trophyButton.cx, app.trophyButton.cy, image=ImageTk.PhotoImage(app.trophyOn))

# for leaderboard screen
def topTen(app):
    bestJumpers = []
    tempDict = copy.deepcopy(app.scoreboard)
    l = len(tempDict)
    return topTenHelper(bestJumpers, tempDict, l)

def topTenHelper(bestJumpers, tempDict, l):
    if len(bestJumpers) == 10:
        return bestJumpers
    elif len(bestJumpers) == l:
        return bestJumpers
    else:
        max = 0
        name = None
        for key in tempDict:
            if tempDict[key] > max:
                max = tempDict[key]
                name = key
        bestJumpers.append((name, max))
        del tempDict[name]
        return topTenHelper(bestJumpers, tempDict, l)

def drawLeaderboard(app, canvas):
    leaders = topTen(app)
    for i in range(len(leaders)):
        canvas.create_text(300, 200+60*i, 
        text = f"{i+1}.) {leaders[i][0]}: {leaders[i][1]} m", 
        font = ("Comic Sans MS", 20))
    canvas.create_text(300, 100, text = "Top 10 Jumpers:", font = ("Comic Sans MS bold", 30))

def drawMenuButton(app, canvas):
    canvas.create_image(app.menuButton.cx, app.menuButton.cy, image=ImageTk.PhotoImage(app.menu))

def drawMenuButtonOn(app, canvas):
    if app.menuIsPressed:
        canvas.create_image(app.menuButton.cx, app.menuButton.cy, image=ImageTk.PhotoImage(app.menuOn))


# for game over screen 
def drawGameOverScreen(app, canvas):
    canvas.create_image(app.gameOverX, app.gameOverY-200, 
                    image = ImageTk.PhotoImage(app.gameOverTitle))
    canvas.create_text(app.gameOverX, app.gameOverY-20, 
                text= f"your height: {app.score} m", font = ("Comic Sans MS", 25))
    # canvas.create_rectangle(app.gameOverX+30, app.gameOverY+20, app.gameOverX+170, app.gameOverY+60)
    canvas.create_text(app.gameOverX, app.gameOverY+40, 
                text = f"your name: {app.playerName}", font = ("Comic Sans MS", 25))
    canvas.create_image(app.gameOverX+180, app.gameOverY+130, image = ImageTk.PhotoImage(app.ttc))

    highScoreHolder, score = highScore(app)
    canvas.create_text(app.gameOverX, app.gameOverY-80, 
        text= f"#1 jumper: {highScoreHolder}: {score} m", font = ("Comic Sans MS", 25))
    

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
    app.nameChangeButton.cy -= abs(app.player.yv)*app.time

def drawPlayAgainButton(app, canvas):
    canvas.create_image(app.playAgainButton.cx, app.playAgainButton.cy, 
                                image=ImageTk.PhotoImage(app.playAgain))
def drawPaButtonIsPressed(app, canvas):
    if app.pabIsPressed == True:
        canvas.create_image(app.playAgainButton.cx, app.playAgainButton.cy, 
                                    image=ImageTk.PhotoImage(app.playAgainOn))

# def drawNameChangeButton(app, canvas):
#     lx, rx, ty, by = app.nameChangeButton.buttonHitbox()
#     canvas.create_rectangle(lx, ty, rx, by)

# rewrite the file to add new player and their score
def reWriteFile(app, name):
    app.scoreboard[name] = app.score
    writeFile('scoreboard.txt', repr(app.scoreboard))

def highScore(app):
    holder = None
    highScore = 0
    for name in app.scoreboard:
        if app.scoreboard[name] > highScore:
            highScore = app.scoreboard[name]
            holder = name
    return holder, highScore

# Mouse functions 
def mousePressed(app, event):
    lx, rx, ty, by = app.playButtonButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.pbIsPressed = True
    
    lx, rx, ty, by = app.trophyButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.trophyPressed = True

    lx, rx, ty, by = app.playAgainButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.pabIsPressed = True

    lx, rx, ty, by = app.menuButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.menuIsPressed = True 

    lx, rx, ty, by = app.nameChangeButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        name = app.getUserInput("Enter your name!\nYour score won't be saved if you don't!")
        if name != None and name != 'Doodler' and name != '':
            app.playerName = name
            reWriteFile(app, name)


def mouseReleased(app, event):
    lx, rx, ty, by = app.playButtonButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.startingMenu = False
        app.playingGame = True
    app.pbIsPressed = False

    lx, rx, ty, by = app.trophyButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.startingMenu = False
        app.leaderboard = True
    app.trophyPressed = False

    lx, rx, ty, by = app.menuButton.buttonHitbox()
    if lx < event.x < rx and ty < event.y < by:
        app.startingMenu = True
        app.leaderboard = False
    app.menuIsPressed = False

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
        drawTrophy(app, canvas)
        drawTrophyOn(app, canvas)
    
    if app.leaderboard:
        drawLeaderboard(app, canvas)
        drawMenuButton(app, canvas)
        drawMenuButtonOn(app, canvas)

    if app.playingGame and app.gameOver != True:
        drawPlatform(app, canvas)
        drawBluePlatform(app, canvas)
        drawBlueHitboxes(app, canvas)
        drawSpring(app, canvas)
        drawBlueMonster(app, canvas)
        drawBullet(app, canvas)
        drawDoodle(app, canvas)  
        # drawPlayerHitbox(app, canvas)
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
        # drawNameChangeButton(app, canvas)


runApp(width = 600, height = 1000)


