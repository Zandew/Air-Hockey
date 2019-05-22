'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         Create the main file to run our air hockey game. This main file contains the program for the
                 user interface of the game. From the main menu the user is able to view the rules of the game,
                 quit the program, and select their choice of level. After selecting their level the user will
                 be able to pause the game, resume the game, and quit the game. Each game lasts for 3 minutes
                 and the players will control their paddles with either the WASD keys or arrow keys. Throughout
                 the game the user will be able to see the score and time remaining. After the 3 minutes of the
                 game are over, the user will be able to see who won or if it was a tie game.
'''

# Modules are imported to invoke their functions
import pygame, time, math, sys

from Paddle import *
from Puck import *
from Goal import *
from GoalBaseBlock import *
from GoalSideBlock import *
from GoalSideBounceBlock import *
from pygame.locals import *

# Initiates pygame.mixer to allow multiple channels for sound effects
pygame.mixer.init(frequency = 22050, size = -16, channels = 4, buffer = 1024)
#pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# Creates the 6 fonts used
# Font for font 1
font1 = pygame.font.SysFont("arial", 48)
# Bolds font 1
font1.set_bold(True)

# Font for font 2
font2 = pygame.font.SysFont("arial", 24)
# Bolds font 2
font2.set_bold(True)

# Font for font 3
font3 = pygame.font.SysFont("arial", 48)
# Bolds font 3
font3.set_bold(True)
# Underlines font 3
font3.set_underline(True)

# Font for font 4
font4 = pygame.font.SysFont("arial", 20)
# Bolds font 4
font4.set_bold(True)
# Underlines font 4
font4.set_underline(True)

# Font for font 5
font5 = pygame.font.SysFont("arial", 20)

# Font for font 6
font6 = pygame.font.SysFont("arial", 28)
# Bolds font 6
font6.set_bold(True)

# Sets the display screen size 
screen = pygame.display.set_mode((1040, 700))

# Creates the different surfaces (e.g. main menu, rules, level selection, game)
# Creates surface for main menu
mainMenu = pygame.Surface((1040, 700))
# Main menu surface colour is set to white
mainMenu.fill((255, 255, 255))

# Creates surface for rules
rules = pygame.Surface((1040, 700))
# Rules surface colour is set to white
rules.fill((255, 255, 255))

# Creates surface for level selection
levelSelection = pygame.Surface((1040, 700))
# Level selection surface is set to white
levelSelection.fill((255, 255, 255))

# Creates background surface
background = pygame.Surface((1040,700))
# Background surface is set to white
background.fill((255, 255, 255))

# Caption for screen
pygame.display.set_caption('Air Hockey')

# Text for back to main menu button (in Rules and Level Selection)
backMainMenu = font1.render("Back to Main Menu", True, (255,255,255))

# Text for after pause button is pressed
resumeText = font6.render("Resume", True, (255,255,255))
quitText = font6.render("Quit", True, (255,255,255))

# Draw the back button to main menu in rules
pygame.draw.rect(rules, (255, 0, 0), pygame.Rect(50, 590, 425, 60))

# Program is originally in main menu
inMenu = True
# Program is not originally in game play
inGame = False
# Program is not originally in rules
inRules = False
# Program is not originally in level selection
inLevelSelection = False
# Game is not originally paused
pause = False
# Game is not originally in level 1
level1 = False
# Game is not originally in level 2
level2 = False
# Game is not originally in the congratulations screen
gameOver = False
# Boolean variable keeps the program running
keep_going = True

# Initialize left goal width, and left goalBaseBlock width
width1 = 200
# Initialize right goal width, and right goalBaseBlock width
width2 = 200

# Initialize the red paddle size
pSize1 = 45
# Initialize the blue paddle size
pSize2 = 45

# Create left goal (Draw out goal)
goal1 = Goal(1, 0, 295, width1)
# Create right goal (Draw out goal)
goal2 = Goal(0, 985, 295, width2)

# Create left goalBaseBlock (Used to detect if a goal is scored)
goalBaseBlock1 = GoalBaseBlock(1, 0, 295, width1)
# Create right goalBaseBlock (Used to detect if a goal is scored)
goalBaseBlock2 = GoalBaseBlock(0, 1029, 295, width2)

# Initialize left goalSideBlock width
sideBlockWidth1 = 150
# Initialize right goalSideBlock width
sideBlockWidth2 = 150

# Create left upper goalSideBlock (Draw side barrier for puck)
goalSideBlockLU = GoalSideBlock(0, 0, 145, sideBlockWidth1)
# Create left lower goalSideBlock (Draw side barrier for puck)
goalSideBlockLL = GoalSideBlock(1, 0, 495, sideBlockWidth1)
# Create right upper goalSideBlock (Draw side barrier for puck)
goalSideBlockRU = GoalSideBlock(2, 985, 145, sideBlockWidth2)
# Create right lower goalSideBlock (Draw side barrier for puck)
goalSideBlockRL = GoalSideBlock(3, 985, 495, sideBlockWidth2)

# Create left upper goalSideBounceBlock (Create side barrier for puck)
goalSideBounceBlockLU = GoalSideBounceBlock(0, 0, 145, sideBlockWidth1)
# Create left lower goalSideBounceBlock (Create side barrier for puck)
goalSideBounceBlockLL = GoalSideBounceBlock(1, 0, 495, sideBlockWidth1)
# Create right upper goalSideBounceBlock (Create side barrier for puck)
goalSideBounceBlockRU = GoalSideBounceBlock(2, 985, 145, sideBlockWidth2)
# Create left lower goalSideBounceBlock (Create side barrier for puck)
goalSideBounceBlockRL = GoalSideBounceBlock(3, 985, 495, sideBlockWidth2)

# Initialize score for player 1
score1 = 0
# Initialize score for player 2
score2 = 0

# Number of increases of goal size
goalIncrease1 = 0
goalIncrease2 = 0

# Loads image for arrow controls in rules
arrowControlImg = pygame.image.load("arrowcontrols.png").convert_alpha()
# Loads image for letter controls in rules
letterControlImg = pygame.image.load("lettercontrols.png").convert_alpha()
# Loads image for air hockey logo in main menu
airHockeyLogo = pygame.image.load("airhockey.png").convert_alpha()
# Loads image for pause button during game play
pauseButton = pygame.image.load("pausebutton.png").convert_alpha()
# Loads image for pause button during game play
exitButton = pygame.image.load("exitbutton.png").convert_alpha()

# Sets the clock for the program
clock = pygame.time.Clock()

# While the program is running
while keep_going:
    clock.tick(60)

    # If in rules screen
    if inRules:

        # Handles the input from users (events)
        for ev in pygame.event.get():

            # If close window button is pressed
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False

            # If mouse is pressed
            elif ev.type == MOUSEBUTTONDOWN:

                # Determines which part of the screen is pressed (coordinates)
                # If back to main menu button is pressed
                if (ev.pos[0]>=50 and ev.pos[0]<=475 and ev.pos[1]>=590 and ev.pos[1]<=650):
                    # Goes back out of rules screen and into main menu screen
                    inRules = False
                    inMenu = True

        # Rules screen title
        rulesTitle = font3.render("RULES", True, (0,0,0))

        # Text for the rules for player with red paddle
        redOutput1 = font4.render("Red Paddle Player Controls:", True, (255,0,0))
        redOutput2 = font5.render("Press 'W' to go up", True, (255,0,0))
        redOutput3 = font5.render("Press 'A' to go left", True, (255,0,0))
        redOutput4 = font5.render("Press 'S' to go down", True, (255,0,0))
        redOutput5 = font5.render("Press 'D' to go right", True, (255,0,0))

        # Text for the rules for player with blue paddle
        blueOutput1 = font4.render("Blue Paddle Player Controls:", True, (0,0,255))
        blueOutput2 = font5.render("Press 'up arrow' to go up", True, (0,0,255))
        blueOutput3 = font5.render("Press 'left arrow' to go left", True, (0,0,255))
        blueOutput4 = font5.render("Press 'down arrow' to go down", True, (0,0,255))
        blueOutput5 = font5.render("Press 'right arrow' to go right", True, (0,0,255))

        # Text for length of each game
        lengthOfGame = font2.render("Each game lasts for 3 minutes.", True, (0,0,0))
        # Text for pausing the game
        pauseGame = font2.render("Click the         button to pause the game, then click either \"Resume\" or \"Quit\".", True, (0,0,0))
        # Text for objective of the game
        objectiveOfGame = font2.render("Objective: Use your paddle to try to hit the puck into your opponent's goal.", True, (0,0,0))
        objectiveOfGame2 = font2.render("The player with the most number of goals wins the game.", True, (0,0,0))

        # Outputs screen for rules
        screen.blit(rules, (0, 0))
        # Outputs rules title
        screen.blit(rulesTitle, (447, 100))
        
        # Outputs text for back to main menu button
        screen.blit(backMainMenu, (60, 593))

        # Outputs image showing controls for red paddle player (letter controls)
        screen.blit(pygame.transform.scale(letterControlImg, (150,100)), (270,200))
        # Outputs image showing controls for blue paddle player (arrow controls)
        screen.blit(pygame.transform.scale(arrowControlImg, (150,100)), (620,200))

        # Output of controls for red paddle player
        screen.blit(redOutput1, (218,175))
        screen.blit(redOutput2, (268,310))
        screen.blit(redOutput3, (268,340))
        screen.blit(redOutput4, (268,370))
        screen.blit(redOutput5, (268,400))

        # Output of controls for blue paddle player
        screen.blit(blueOutput1, (568,175))
        screen.blit(blueOutput2, (598,310))
        screen.blit(blueOutput3, (598,340))
        screen.blit(blueOutput4, (598,370))
        screen.blit(blueOutput5, (598,400))

        # Output of length of each game
        screen.blit(lengthOfGame, (355,430))
        # Output for pausing the game instructions
        screen.blit(pauseGame, (105,465))
        # Output for objective of the game
        screen.blit(objectiveOfGame, (130,500))
        screen.blit(objectiveOfGame2, (220,535))

        # Outputs pause button
        screen.blit(pygame.transform.scale(pauseButton, (40,40)), (207.5,460))
        # Outputs air hockey logo at the top of the screen
        screen.blit(pygame.transform.scale(airHockeyLogo, (312,120)), (364,0))

    # If in main menu screen
    elif inMenu:

        # Handles the input from users (events)
        for ev in pygame.event.get():

            # If close window button is pressed
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False

            # If mouse is pressed
            elif ev.type == MOUSEBUTTONDOWN:
                
                # Determines which part of the screen is pressed (coordinates)
                # If level selection button is pressed
                if (ev.pos[0]>=100 and ev.pos[0]<=500 and ev.pos[1]>=200 and ev.pos[1]<=400):
                    # Goes out of main menu screen and into level selection screen
                    inMenu = False
                    inLevelSelection = True

                # If rules button is pressed
                elif (ev.pos[0]>=540 and ev.pos[0]<=940 and ev.pos[1]>=200 and ev.pos[1]<=400):
                    # Goes out of main menu screen and into rules screen
                    inMenu = False
                    inRules = True
                    
                # If exit button is pressed
                elif (ev.pos[0]>=445 and ev.pos[0]<=595 and ev.pos[1]>=430 and ev.pos[1]<=485):
                    # Quits and closes program
                    pygame.quit()
                    sys.exit()
                    keep_going = False

        # Creates rectangle for level selection button
        pygame.draw.rect(mainMenu, (0, 0, 255), pygame.Rect(100, 200, 400, 200))
        # Creates rectangle for rules button
        pygame.draw.rect(mainMenu, (0,205,0), pygame.Rect(540, 200, 400, 200))
        
        # Text for level selection button (in Main Menu)
        levelSelectionMenu = font1.render("Level Selection", True, (255,255,255))
        # Text for rules button (in Main Menu)
        rulesMenu = font1.render("Rules", True, (255,255,255))

        # Main menu title (in Main Menu)
        mainTitle = font3.render("MAIN MENU", True, (0,0,0))
        
        # Outputs screen for main menu
        screen.blit(mainMenu, (0, 0))
        # Outputs main menu title
        screen.blit(mainTitle, (389, 100))
        # Outputs text for level selection button
        screen.blit(levelSelectionMenu, (135, 271))
        # Outputs text for rules button (in Main Menu)
        screen.blit(rulesMenu, (680, 271))

        # Outputs exit propgram button
        screen.blit(pygame.transform.scale(exitButton, (150,55)), (445,430))
        # Outputs air hockey logo
        screen.blit(pygame.transform.scale(airHockeyLogo, (780,300)), (130,450))

    # If in level selection screen
    elif inLevelSelection:
        
        # Handles the input from users (events)
        for ev in pygame.event.get():

            # If close window button is pressed
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False

            # If mouse is pressed
            elif ev.type == MOUSEBUTTONDOWN:

                # Determines which part of the screen is pressed (coordinates)
                # If back to main menu button is pressed
                if (ev.pos[0]>=50 and ev.pos[0]<=475 and ev.pos[1]>=590 and ev.pos[1]<=650):
                    # Goes out of level selection screen and into main menu screen
                    inLevelSelection = False
                    inMenu = True

                # If level 1 button is pressed
                elif (ev.pos[0]>=100 and ev.pos[0]<=500 and ev.pos[1]>=200 and ev.pos[1]<=400):
                    # Goes to out of level selection and into game (game is in level 1)
                    inLevelSelection = False
                    level1 = True
                    inGame = True
                    gameOver = False

                    # Start time to calculate the time remaining in the game
                    startTime = time.time()

                    # Original red paddle size
                    pSize1 = 60
                    # Original blue paddle size
                    pSize2 = 60

                    # Outputs original positions of the paddles and puck
                    p1 = Paddle("redpaddle.png", 1, 145, 55, 645, 520, pSize1)
                    p2 = Paddle("bluepaddle.png", 0, 145, 520, 645, 985, pSize2)
                    puck = Puck("puck.png", 145, 10, 645, 1030, 45)
                    
                    # Initialize score for player 1
                    score1 = 0
                    # Initialize score for player 2
                    score2 = 0

                    # Number of increases of goal size
                    goalIncrease1 = 0
                    goalIncrease2 = 0

                    # Initialize left goal width, and left goalBaseBlock width
                    width1 = 200
                    # Initialize right goal width, and right goalBaseBlock width
                    width2 = 200
                    # Create left goal
                    goal1 = Goal(1, 0, 295, width1)
                    # Create right goal
                    goal2 = Goal(0, 985, 295, width2)
                    # Create left goalBaseBlock
                    goalBaseBlock1 = GoalBaseBlock(1, 0, 295, width1)
                    # Create right goalBaseBlock
                    goalBaseBlock2 = GoalBaseBlock(0, 1029, 295, width2)
                    # Initialize left goalSideBlock width
                    sideBlockWidth1 = 150
                    # Initialize rigth goalSideBlock width
                    sideBlockWidth2 = 150
                    # Create left upper goalSideBlock
                    goalSideBlockLU = GoalSideBlock(0, 0, 145, sideBlockWidth1)
                    # Create left lower goalSideBlock
                    goalSideBlockLL = GoalSideBlock(1, 0, 495, sideBlockWidth1)
                    # Create right upper goalSideBlock
                    goalSideBlockRU = GoalSideBlock(2, 985, 145, sideBlockWidth2)
                    # Create right lower goalSideBlock
                    goalSideBlockRL = GoalSideBlock(3, 985, 495, sideBlockWidth2)
                    # Create left upper goalSideBounceBlock
                    goalSideBounceBlockLU = GoalSideBounceBlock(0, 0, 145, sideBlockWidth1)
                    # Create left lower goalSideBounceBlock
                    goalSideBounceBlockLL = GoalSideBounceBlock(1, 0, 495, sideBlockWidth1)
                    # Create right upper goalSideBounceBlock
                    goalSideBounceBlockRU = GoalSideBounceBlock(2, 985, 145, sideBlockWidth2)
                    # Create left lower goalSideBounceBlock
                    goalSideBounceBlockRL = GoalSideBounceBlock(3, 985, 495, sideBlockWidth2)

                # If level 2 button is pressed
                elif (ev.pos[0]>=540 and ev.pos[0]<=940 and ev.pos[1]>=200 and ev.pos[1]<=400):
                    # Goes to out of level selection and into game (game is in level 2)
                    inLevelSelection = False
                    level2 = True
                    inGame = True
                    gameOver = False

                    # Start time to calculate the time remaining in the game
                    startTime = time.time()

                    # Original red paddle size
                    pSize1 = 60
                    # Original blue paddle size
                    pSize2 = 60

                    # Outputs original positions of the paddles and puck
                    p1 = Paddle("redpaddle.png", 1, 145, 55, 645, 520, pSize1)
                    p2 = Paddle("bluepaddle.png", 0, 145, 520, 645, 985, pSize2)
                    puck = Puck("puck.png", 145, 10, 645, 1030, 45)
                    
                    # Initialize score for player 1
                    score1 = 0
                    # Initialize score for player 2
                    score2 = 0

                    # Number of increases of goal size
                    goalIncrease1 = 0
                    goalIncrease2 = 0

                    # Initialize left goal width, and left goalBaseBlock width
                    width1 = 200
                    # Initialize right goal width, and right goalBaseBlock width
                    width2 = 200
                    # Create left goal
                    goal1 = Goal(1, 0, 295, width1)
                    # Create right goal
                    goal2 = Goal(0, 985, 295, width2)
                    # Create left goalBaseBlock
                    goalBaseBlock1 = GoalBaseBlock(1, 0, 295, width1)
                    # Create right goalBaseBlock
                    goalBaseBlock2 = GoalBaseBlock(0, 1029, 295, width2)
                    # Initialize left goalSideBlock width
                    sideBlockWidth1 = 150
                    # Initialize rigth goalSideBlock width
                    sideBlockWidth2 = 150
                    # Create left upper goalSideBlock
                    goalSideBlockLU = GoalSideBlock(0, 0, 145, sideBlockWidth1)
                    # Create left lower goalSideBlock
                    goalSideBlockLL = GoalSideBlock(1, 0, 495, sideBlockWidth1)
                    # Create right upper goalSideBlock
                    goalSideBlockRU = GoalSideBlock(2, 985, 145, sideBlockWidth2)
                    # Create right lower goalSideBlock
                    goalSideBlockRL = GoalSideBlock(3, 985, 495, sideBlockWidth2)
                    # Create left upper goalSideBounceBlock
                    goalSideBounceBlockLU = GoalSideBounceBlock(0, 0, 145, sideBlockWidth1)
                    # Create left lower goalSideBounceBlock
                    goalSideBounceBlockLL = GoalSideBounceBlock(1, 0, 495, sideBlockWidth1)
                    # Create right upper goalSideBounceBlock
                    goalSideBounceBlockRU = GoalSideBounceBlock(2, 985, 145, sideBlockWidth2)
                    # Create left lower goalSideBounceBlock
                    goalSideBounceBlockRL = GoalSideBounceBlock(3, 985, 495, sideBlockWidth2)

        # Draw the back button to main menu in levelSelection
        pygame.draw.rect(levelSelection, (255, 0, 0), pygame.Rect(50, 590, 425, 60))

        # Draw the button for the Level 1 button and Level 2 button respectively
        pygame.draw.rect(levelSelection, (0,201,87), pygame.Rect(540, 200, 400, 200))
        pygame.draw.rect(levelSelection, (0,191,255), pygame.Rect(100, 200, 400, 200))
        
        # Level selection title
        levelSelectionTitle = font3.render("LEVEL SELECTION", True, (0,0,0))
        # Text for buttons during level selection
        levelOneTitle = font1.render("Level 1", True, (255,255,255))
        levelTwoTitle = font1.render("Level 2", True, (255,255,255))

        # Text to describe each level
        levelOneDescription1 = font6.render("Opponent's goal size increases", True, (255,255,255))
        levelOneDescription2 = font6.render("when player scores.", True, (255,255,255))
        levelTwoDescription1 = font6.render("Player's paddle size increases", True, (255,255,255))
        levelTwoDescription2 = font6.render("when player scores.", True, (255,255,255))
        
        # Outputs level selection screen
        screen.blit(levelSelection, (0, 0))
        # Outputs level selection title
        screen.blit(levelSelectionTitle, (312, 100))
        
        # Outputs text for each button (Level 1 and Level 2)
        screen.blit(levelOneTitle, (225, 271))
        screen.blit(levelTwoTitle, (660, 271))

        # Outputs description of each level
        screen.blit(levelOneDescription1, (115, 330))
        screen.blit(levelOneDescription2, (181, 360))
        screen.blit(levelTwoDescription1, (560, 330))
        screen.blit(levelTwoDescription2, (623, 360))

        # Outputs air hockey logo at the top of the screen
        screen.blit(pygame.transform.scale(airHockeyLogo, (312,120)), (364,0))
        
        # Outputs text for back to main menu button
        screen.blit(backMainMenu, (60, 593))

    # If air hockey game is paused
    elif pause:

        # Handles the input from users (events)
        for ev in pygame.event.get():

            # If close window button is pressed
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False

            # If mouse is pressed
            elif ev.type == MOUSEBUTTONDOWN:

                # Determines which part of the screen is pressed (coordinates)
                # If resume button is pressed
                if (ev.pos[0]>=445 and ev.pos[0]<=595 and ev.pos[1]>=270 and ev.pos[1]<=370):
                    # Game continues from where it left off (game is no longer paused)
                    inGame = True
                    pause = False
                    
                    # Calculate the amount of time paused (allow the game to continue on from the time when it was paused)
                    pausedTime = time.time() - pauseStartTime
                    startTime += pausedTime

                # If quit button is pressed
                elif (ev.pos[0]>=445 and ev.pos[0]<=595 and ev.pos[1]>=419 and ev.pos[1]<=519):
                    # Goes to main menu screen from game screen (game is no longer paused)
                    inMenu = True
                    inGame = False
                    pause = False

                    # After quitting the game, it is neither in level 1 nor level 2
                    if level1:
                        level1 = False
                    else:
                        level2 = False

        # Output of the pause screen
        pygame.draw.rect(screen, (41,41,41), pygame.Rect(420, 245, 200, 300))
        # Button for resume game
        pygame.draw.rect(screen, (28,134,238), pygame.Rect(445, 270, 150, 100))
        # Button for quit game      
        pygame.draw.rect(screen, (255,48,48), pygame.Rect(445, 419, 150, 100))
        # Text for resume button
        screen.blit(resumeText, (470,302.5))
        # Text for quit button
        screen.blit(quitText, (493,450))

    elif gameOver:

        # Handles the input from users (events)
        for ev in pygame.event.get():
            # If close window button is pressed
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False

            # If mouse is pressed
            elif ev.type == MOUSEBUTTONDOWN:

                # If main menu button during game over is pressed
                if (ev.pos[0]>=420 and ev.pos[0]<=620 and ev.pos[1]>=425 and ev.pos[1]<=500):
                    # Goes out of the game and into main menu
                    inGame = False
                    inMenu = True

        # If red paddle player wins
        if score2 > score1:
            # Text for game over and red wins
            winner1 = font1.render("Game Over!", True, (255,255,255))
            winner2 = font1.render("Red Wins!", True, (255,255,255))
        # If blue paddle player wins
        elif score1 > score2:
            # Text for game over and blue wins
            winner1 = font1.render("Game Over!", True, (255,255,255))
            winner2 = font1.render("Blue Wins!", True, (255,255,255))
        # If tie game
        else:
            # Text for game over and tie game
            tie1 = font1.render("Game Over!", True, (255,255,255))
            tie2 = font1.render("Tie Game!", True, (255,255,255))

        # Text for button from game to main menu
        gameToMenuText = font6.render("Main Menu", True, (255,255,255))
        # Rectangle for game over background
        pygame.draw.rect(screen, (0,201,87), pygame.Rect(320, 245, 400, 300))
        # Rectangle for main menu button
        pygame.draw.rect(screen, (255,48,48), pygame.Rect(420, 425, 200, 75))
        screen.blit(gameToMenuText, (455,445))

        # Output if there is a winner
        if score2 > score1 or score1 > score2:
            screen.blit(winner1, (390,300))
            screen.blit(winner2, (405,350))
        # Output if tie game
        else:
            screen.blit(tie1, (390,300))
            screen.blit(tie2, (410,350))
            
    else:

        # Handles the input from users (events)
        for ev in pygame.event.get():

            # Handles the input from users (events)
            if ev.type == QUIT:
                # Quits and closes program
                pygame.quit()
                sys.exit()
                keep_going = False
                
            # If pause button is pressed
            elif ev.type == MOUSEBUTTONDOWN:

                # Determines which part of the screen is pressed (coordinates)
                # If paused button is pressed
                if (ev.pos[0]>=25 and ev.pos[0]<=75 and ev.pos[1]>=25 and ev.pos[1]<=75):
                    # Game is paused
                    pause = True
                    inGame = False
                    # Determines the time when game is paused (used to determine what time to start at if the game resumes)
                    pauseStartTime = time.time()

        # 3 minute timer for the game
        gameTime = 180-(round(time.time() - (startTime)))
        # If game is over
        if gameTime == 0:
            # Buzzer sound is played
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("buzzer.wav"))
            # Goes out of game and into congratulations screen
            inGame = False
            gameOver = True
            
           # After the game ends, it is neither in level 1 nor level 2
            if level1:
                level1 = False
            else:
                level2 = False
            
        # Determines number of minutes left
        minuteTime = gameTime // 60
        # Determines number of seconds left
        secondTime = gameTime % 60
        # Output of time on game screen
        stringTime = str(minuteTime) + ":"

        # Formatting the time
        # If less than 10 seconds of the minute is left
        if (secondTime<10):
            stringTime += "0"+str(secondTime)
        # If 10 or more seconds of the minute is left
        else:
            stringTime += str(secondTime)
        
        # Output the time remaining for the game
        timeOutput = font1.render(stringTime, True, (255,0,0))
        # Output the score for the game
        scoreOutput = font1.render((str(score2) + " : " + str(score1)), True, (0,0,255))

        # Determines which key is pressed by the user to control their paddle
        keys = pygame.key.get_pressed()

        # Gets the input from the user for controlling the paddle and uses Paddle class
        p1.update(keys)
        p2.update(keys)

        # If player 1 collides with the puck
        if (p1.collide(puck)):
            puck.bounce(p1)
        # If player 2 collides with the puck
        if (p2.collide(puck)):
            puck.bounce(p2)
 
        # If the puck collides with the left goal (blue paddle player scores)
        if goalBaseBlock1.get_rect().colliderect(puck):
            # Goal sound is played
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("goal.wav"))

            # If game is in level 1
            if level1:
                # Width of the goal size increases up to certain size
                if width1 < 401:
                    width1 += 40
                    # Blocks beside the goal decreases because of goal size increase
                    sideBlockWidth1 -= 20
                    # Number of goal size increases (variable used in calculations to centre goal and increase circle around goal)
                    goalIncrease1 += 1
            # If game is in level 2
            else:
                if pSize2 < 120:
                    pSize2 += 10

            # Paddles and puck are reset to original positions
            p1 = Paddle("redpaddle.png", 1, 145, 55, 645, 520, pSize1)
            p2 = Paddle("bluepaddle.png", 0, 145, 520, 645, 985, pSize2)
            puck = Puck("puck.png", 145, 10, 645, 1030, 45)

            '''
            # Text if goal size can no longer be adjusted
            maxIncreaseLabel2 = font2.render("Goal Size Maximum", True, (50,205,50))
            '''
            
            # Use the Goal class to create left goal (also centres the left goal)
            goal1 = Goal(1, 0, (100+((690-100)/2)-(width1/2)), width1)

            # Use the GoalBaseBlock class to create block in left goal to determine when the puck enters the goal (used so that the puck enters the goal entirely before goal is scored)
            goalBaseBlock1 = GoalBaseBlock(1, 0,(100+((690-100)/2)-(width1/2)), width1)

            # Use the GoalSideBlock class to draw upper block beside left goal and adjusts the width of the block in accordance of the goal size
            goalSideBlockLU = GoalSideBlock(0, 0, 145, sideBlockWidth1)
            # Use the GoalSideBounceBlock class to create upper block beside left goal and adjusts the width of the block in accordance of the goal size (used to create puck barrier)
            goalSideBounceBlockLU = GoalSideBounceBlock(0, 0, 145, sideBlockWidth1)
            
            # Use the GoalSideBlock class to draw lower block beside left goal and adjusts the width of the block in accordance of the goal size
            goalSideBlockLL = GoalSideBlock(1, 0, (495 + goalIncrease1*20), sideBlockWidth1)
            # Use the GoalSideBounceBlock class to create lower block beside left goal and adjusts the width of the block in accordance of the goal size (used to create puck barrier)
            goalSideBounceBlockLL = GoalSideBounceBlock(1, 0, (495 + goalIncrease1*20), sideBlockWidth1)

            # Increases score of blue paddle player
            score1 += 1
            # Pauses screen for 2 seconds to allow time for clapping sound effect
            time.sleep(2)
            # Allows game to continue from time that goal is scored
            startTime += 2

        # If the puck collides with the right goal (red paddle player scores)
        if goalBaseBlock2.get_rect().colliderect(puck):
            # Goal sound is played
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("goal.wav"))

            # If game is in level 1
            if level1:
                # Width of the goal size increases up to certain size
                if width2 < 401:
                    width2 += 40
                    # Blocks beside the goal decreases because of goal size increase
                    sideBlockWidth2 -= 20
                    # Number of goal size increases (variable used in calculations to centre goal and increase circle around goal)
                    goalIncrease2 += 1
            # If game is in level 2
            else:
                if pSize1 < 120:
                    pSize1 += 10

            # Paddles and puck are reset to original positions
            p1 = Paddle("redpaddle.png", 1, 145, 55, 645, 520, pSize1)
            p2 = Paddle("bluepaddle.png", 0, 145, 520, 645, 985, pSize2)
            puck = Puck("puck.png", 145, 10, 645, 1030, 45)

            '''
            # Text if goal size can no longer be adjusted
            maxIncreaseLabel1 = font2.render("Goal Size Maximum", True, (50,205,50))
            '''
            # Use the Goal class to create right goal (also centres the right goal)
            goal2 = Goal(0, 985, (100+((690-100)/2)-(width2/2)), width2)

            # Use the GoalBaseBlock class to create block in right goal to determine when the puck enters the goal (used so that the puck enters the goal entirely before goal is scored)
            goalBaseBlock2 = GoalBaseBlock(0, 1029,(100+((690-100)/2)-(width2/2)), width2)

            # Use the GoalSideBlock class to draw upper block beside right goal and adjusts the width of the block in accordance of the goal size
            goalSideBlockRU = GoalSideBlock(2, 985, 145, sideBlockWidth2)
            # Use the GoalSideBounceBlock class to create upper block beside right goal and adjusts the width of the block in accordance of the goal size (used to create puck barrier)
            goalSideBounceBlockRU = GoalSideBounceBlock(2, 985, 145, sideBlockWidth2)

            # Use the GoalSideBlock class to draw lower block beside right goal and adjusts the width of the block in accordance of the goal size
            goalSideBlockRL = GoalSideBlock(3, 985, (495 + goalIncrease2*20), sideBlockWidth2)
            # Use the GoalSideBounceBlock class to create lower block beside right goal and adjusts the width of the block in accordance of the goal size (used to create puck barrier)
            goalSideBounceBlockRL = GoalSideBounceBlock(3, 985, (495 + goalIncrease2*20), sideBlockWidth2)

            # Increases score of red paddle player
            score2 += 1
            # Pauses screen for 2 seconds to allow time for clapping sound effect
            time.sleep(2)
            # Allows game to continue from time that goal is scored
            startTime += 2

        # If puck collides with the block beside the left goal
        if goalSideBounceBlockLU.get_rect().colliderect(puck) or goalSideBounceBlockLL.get_rect().colliderect(puck):
            # If puck is greater than 0.2, puck decelerates
            if (puck.speed>0.2):
                puck.speed -= 0.2
            # Else puck stops moving
            else:
                puck.speed = 0

            # Movement of the puck when it collides with the block
            puck.rect.move_ip(math.cos(puck.angle)*puck.speed, -math.sin(puck.angle)*puck.speed)
            puck.angle = calibrate(puck.angle)

            # Wall sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            if (puck.angle<math.pi):
                puck.angle = math.pi-puck.angle
            else:
                puck.angle = math.pi*2-puck.angle-math.pi
            puck.rect.move_ip(math.cos(puck.angle)*puck.speed, -math.sin(puck.angle)*puck.speed)

        # If puck collides with the bottom side of the upper left side block (so the puck does not get stuck in the upper left side block)
        if (puck.xmin < 55 and goalSideBounceBlockLU.get_rect().colliderect(puck)):
            # Puck is bounced to the outside of the goal
            puck.xmin = 56
            puck.ymin = sideBlockWidth1 + 1
            puck.update()
            # Puck barrier coordinates are set back to original 
            puck.xmin = 10
            puck.ymin = 145
        # If puck collides with top side of the lower left side block (so the puck does not get stuck in the lower left side block)
        elif (puck.xmin < 55 and goalSideBounceBlockLL.get_rect().colliderect(puck)):
            # Puck is bounced to outside of the goal
            puck.xmin = 56
            puck.ymin = 645 - sideBlockWidth1 - 45 - 1
            puck.update()
            # Puck barrier coordinates are set back to original
            puck.xmin = 10
            puck.ymin = 145

        # If puck collides with the block beside the right goal
        if goalSideBounceBlockRU.get_rect().colliderect(puck) or goalSideBounceBlockRL.get_rect().colliderect(puck):
            # If puck is greater than 0.2, puck decelerates
            if (puck.speed>0.2):
                puck.speed -= 0.2
            # Else puck stops moving
            else:
                puck.speed = 0

            # Movement of the puck when it collides with the block
            puck.rect.move_ip(math.cos(puck.angle)*puck.speed, -math.sin(puck.angle)*puck.speed)
            puck.angle = calibrate(puck.angle)

            # Wall sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))
            
            if (puck.angle<math.pi/2):
                puck.angle = math.pi-puck.angle
            else:
                puck.angle = math.pi*2-puck.angle+math.pi
            puck.rect.move_ip(math.cos(puck.angle)*puck.speed, -math.sin(puck.angle)*puck.speed)

        # If puck collides with the bottom side of the upper right side block (so the puck does not get stuck in the upper right side block)
        if (puck.xmax > 985 and goalSideBounceBlockRU.get_rect().colliderect(puck)):
            # Puck is bounced to outside of the goal
            puck.xmax = 984
            puck.ymin = sideBlockWidth1 + 1
            puck.update()
            # Puck barrier coordinates are set back to original
            puck.xmax = 1030
            puck.ymin = 145
        # If puck collides with top side of the lower right side block (so the puck does not get stuck in the lower right side block)
        elif (puck.xmax > 985 and goalSideBounceBlockRL.get_rect().colliderect(puck)):
            # Puck is bounced to outside of the goal
            puck.xmax = 984
            puck.ymin = 645 - sideBlockWidth1 - 45 - 1
            puck.update()
            # Puck barrier coordinates are set back to original
            puck.xmax = 1030
            puck.ymin = 145
            
        # Size for top and bottom border of air hockey surface
        recSize = (1040,55)
        
        # Top border
        recSideTop = pygame.Surface(recSize).convert()
        # Bottom border
        recSideBottom = pygame.Surface(recSize).convert()
        
        # Colour all top and bottom borders brown
        recSideTop.fill((138,54,15))
        recSideBottom.fill((138,54,15))

        puck.update()

        # Makes the background of the air hockey game surface white
        screen.blit(background, (0, 0))
        # Draw centre line of air hockey surface
        pygame.draw.line(screen, (255,0,0), (519,100), (519,690),5)
        
        # Draw circles at centre of air hockey surface
        pygame.draw.circle(screen, (255,0,0), (520, 395), 130)
        pygame.draw.circle(screen, (255,255,255), (520, 395), 125)

        # Draw semicircles at left goal
        pygame.draw.circle(screen, (255,0,0), (15, 395), 105+(goalIncrease1*20))
        pygame.draw.circle(screen, (255,255,255), (15, 395), 100+(goalIncrease1*20))

        # Draw semicircles at right goal
        pygame.draw.circle(screen, (255,0,0), (1025, 395), 105+(goalIncrease2*20))
        pygame.draw.circle(screen, (255,255,255), (1025, 395), 100+(goalIncrease2*20))

        # Outputs the paddles and puck to the screen
        screen.blit(p1.image, p1.rect)
        screen.blit(p2.image, p2.rect)
        screen.blit(puck.image, puck.rect)

        # Outputs the borders of the air hockey surface
        # Top border
        screen.blit(recSideTop, (0,90))
        # Bottom border
        screen.blit(recSideBottom, (0,645))
        # Upper left goal side block
        screen.blit(goalSideBlockLU.image, goalSideBlockLU.rect)
        # Lower left goal side block
        screen.blit(goalSideBlockLL.image, goalSideBlockLL.rect)
        # Upper right goal side block
        screen.blit(goalSideBlockRU.image, goalSideBlockRU.rect)
        # Lower right goal side block
        screen.blit(goalSideBlockRL.image, goalSideBlockRL.rect)

        # Outputs the pause button
        screen.blit(pygame.transform.scale(pauseButton, (50,50)), (25,25))

        # Outputs the goals of the air hockey surface
        screen.blit(goal1.image, goal1.rect)
        screen.blit(goal2.image, goal2.rect)

        # Outputs the time remaining
        screen.blit(timeOutput, (475,0))

        # Centres the output of the score on the screen
        if score2 < 10:
            screen.blit(scoreOutput, (472,40))
        elif score2 >= 10:
            screen.blit(scoreOutput, (446,40))
        
        # Outputs of "Goal Size Maximum" text if the left goal reaches its maximum size
        if width1 > 400:
            screen.blit(font2.render("Goal Size Maximum", True, (50,205,50)), (90,60))
        # Outputs of "Goal Size Maximum" text if the right goal reaches its maximum size
        if width2 > 400:
            screen.blit(font2.render("Goal Size Maximum", True, (50,205,50)), (740,60))

        # Outputs of "Paddle Size Maximum" text if the red paddle reaches its maximum size
        if pSize1 == 120:
            screen.blit(font2.render("Paddle Size Maximum", True, (50,205,50)), (90, 60))
        # Outputs of "Paddle Size Maximum" text if the blue paddle reaches its maximum size
        if pSize2 == 120:
            screen.blit(font2.render("Paddle Size Maximum", True, (50,205,50)), (740, 60))

        # If game is in level 1, level 1 is shown on the screen during game play so that the users know which level they are playing in        
        if level1:
            screen.blit(font6.render("LEVEL 1", True, (0,191,255)), (250, 25))
        # If game is in level 2, level 1 is shown on the screen during game play so that the users know which level they are playing in  
        else:
            screen.blit(font6.render("LEVEL 2", True, (0,139,0)), (250, 25))

    # Updates the full display surface to the screen
    pygame.display.flip()
