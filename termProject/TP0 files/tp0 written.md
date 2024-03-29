                        TP0: Project Overview
                            Game: 112 Jump

Project Description:
    The game I will be creating will be called "112 Jump." It is an infinite 
vertical jumper that is very similar to the famous mobile game "Doodle Jump."
This will be a single player game, and the character will be controlled by the 
the right and left arrow keys (to move left and right), and the space bar (to 
shoot upwards). The goal is to move the character onto platforms and jump to 
the next platform and go as high as possible. The screen follows you as you go
higher, but the amount of platforms decreases over time. There will be multiple 
different types of platforms and enemies that can knock you off. Coming into 
contact with said enemies will cause you to lose, but you can avoid them or 
shoot them to remove them. Also, missing platforms will cause you to fall, also
making you lose. Lastly, there will be some power ups that let you go higher, 
such as a jet pack and a helicopter hat. 


Similar Projects:
    After researching online, I found multiple similar projects and tutorial 
videos done on an "Infinite Vertical Jumper"-most of them being Doodle Jump. 
One project I came across was a tutorial video utilizing pyGame to create this 
game: https://www.youtube.com/watch?v=qmcgrk5KfHQ. There are multiple things 
aspects of code that I will do differently than the creator in this video. 
The biggest differences between my own project and his will be Object Oriented 
Programming and also the utilization of PyGame. He did not use OOP in his 
tutorial, however, I will make classes and different files to format my game. 
Also, he used PyGame, but I will be creating the game from bare bones: I will 
create all aspects of the game myself other than the pictures of the sprites. 
    Another project I found was also a tutorial video, however, it was done on 
MIT's Scratch Website. Scratch is an online drag and drop platform that allows
for beginner friendly programming, but there is still a high ceiling to what 
can be done on the website. In this video, a barebones infinite jumper was made:
https://www.youtube.com/watch?v=OjHGgsg7xgM. The major differences with my code 
will be that I will actually have to program out all of the smaller parts that 
Scratch offers a short cut to. The tutorial did use some object oriented code 
since Scratch makes it easy to separate programs by Sprites, and although the 
many of the major ideas will actually be similar, my program will be much more 
intensive than the scratch project. Some minor differences I also noticed were 
that his project used the mouse position to move, and mine will be arrow keys. 

Structural Plan:
    HACK112 was excellent practice for me to learn and figure out how I can 
properly utilize Object Oriented Programming. I will definitely be using OOP in 
this game because it demonstrated to me how I can split the game up into classes 
and solve each problem one at a time. At the end, they will all come together in
my main.py file, and by then I should have a pretty working game! 
    Like I said before, I want to split "112 Jump" into different classes and 
solve the problems one at a time. I will list off as many classes as I can think
of, but I may miss a few classes/functions. 
    1. main.py 
      - main python file that will import each class and actually 
        run the game
      - start and end screen will be in main as well as score 
    2. Player Class 
      - here I will import and create the player sprite 
      - add the key pressed functions to move the sprite left/right and shoot 
      - can either shoot with space bar(bullet moves straight up), or can click
        mouse to aim it 
      - I think I'll add option to use "a" and "d" as left and right to make it
        easier to use mouse
      - Player will have a hitbox and something to keep track of x/y coords
    3. Platform Class 
      - platforms will spawn randomly
      - at the beginning there will be many platforms, but over time the amount 
        on the screen decreases
      - three different types: blue, green, and broken 
            - blue moves right and left 
            - green does not move 
            - player falls through broken platforms (brown and cracked)
      - there must be at least one platform that the player can reach 
            - will need to use math to make sure of this 
            - when velocity = 0 (aka top of jump) there must be a platform
      - will need hitboxes so that character jumps each time it hits 
    4. Enemy Class 
      - enemies begin to spawn randomly at a certain height 
      - have a hitbox, if the player comes in contact then the player falls  
        through all platforms and loses(goes to game over screen)
      - if enemy is shot, it disappears
      - some of the enemies move left and right a little bit 
    5. Physics Class 
      - will have the physics of the game 
      - Gravity: 1/2gt^2 + v0t + h0
      - The character will have perfectly elastic collisions with platforms:
            m1v1 + m2v2 = m1v1 + m2v2 (v2 will be 0 because its a platform)
            m1v1 = m1(-v1) 
      - Q: Should I make Physics as a class or put it in main? 
    6. PowerUps Class
      - There will be 3 different boosts that will spawn:
            - a spring: springs will appear randomly on some platforms and it 
              gives you a super jump
            - a helicopter hat: you will become a lil mini helicopter and get a 
              nice flight upwards 
            - a jetpack: you will equip a jetpack and get the biggest boost 
              upwards 
    7. GameOver Class
      - If the player goes below the lowest platform, it follows the character
        and simultaneously goes to the game over screen 


Algorithmic Plan:
    I think the trickiest part of the project will be implementing the physics 
and the math required to ensure that there is always a possible platform that 
the player can reach, to ensure that the player is always bouncing up and down.
Also, I think that spawning more enemies as height goes up while spawning less 
platforms will be difficult. 
    Other than the physics, I don't think it will be too difficult to keep track
of the platforms, shooting, or enemies, because I will be able to store those in
lists and draw them that way (similar to the Bubbles problem that was a practice 
problem when we were doing graphics). 
    However, in order to implement the physics and math, I will probably do many
smaller test files where I test out if my elasticity and gravity works. I think 
I will have to keep track of dx, dy, and acceleration of the player character 
in order to implement the gravity and elasticity. That will also help me keep
track of the top of the jump and how high that is. Furthermore, I will need to 
give each platform an cx and cy coord to draw it at. Over time, I will have the 
distance between one platform to the next get closer to that maximum value. I 
think this can be done by calculating that height and then using a randint that 
spawns the platforms, but also a small incrementer that increments the possible
height between the previous platforms and the next by an amount over time. Also, 
in order to keep it smooth, I think I will spawn the platforms a certain distance 
above the screen and despawn the ones that go below in order to have the best     
user interface. 


Timeline Plan:
    11/20/22:
        - Create Player Class and get game Physics Class working together
        - also be able to run them through main and get some basic platforms 
          to spawn (without math)
        - import the background and all sprites 
        - basically have some barebones code that has a jumper game
    11/30/22: 
        - add complexity to the platform spawns and make sure they despawn
          as they leave the screen to make it more difficult
        - also add the other two types of platforms (moving and broken)
        - create Enemy Class and have them spawn occassionally after a certain 
          height
        - probably have simple enemies that don't move at first just to meet MVP
        - Implement shooting from the player (only straight up here)
        - goal at this point is to reach mvp, although it might not be the 
          best or prettiest looking yet
    12/5/22:
        - add power ups and make enemies more complex (moving)
        - finish PowerUp Class and GameOver Class
        - work hard on front-end design aspects:
            - create a nice menu screen that shows the character bouncing
              up and down 
                - play button, and possibly menu button that can change sprites 
                and the themes 
                - buttons change color when hovered over
                - looks visually appealing and has nice title and background
                - when you press play, there is a smooth transition to the game
            - create a good Game Over screen where it follows you as you fall 
              off and then shows the game over screen after passing the bottom-
              most platform 
        - clean up code and play game a lot to check for issues that need 
          to be debugged 
        - review all concepts used and make sure to have a nice presentation! 
        - make sure that score works and all of the things fit into main  
        - possibly change shooting to aim at where the mouse is at and 
          shoots when mouse clicked
            - if implemented, also let user move left/right with "a" and "d"

Version Control Plan: 
    I plan on using google drive to back up all of my game files. I will copy 
and paste the code onto a google docs file and keep it catagorized by TP0, TP1, 
TP2, TP3. I will also have a separate folder where I keep the latest working 
code. An attachment is in this zip file of how I will do so. 


Module List:
    As of right now, I am planning on creating this project from scratch. I will 
only be using cmu_112_graphics and my brain to create 112 Jump! 


StoryBoard:
    Attached in the zip file. 
