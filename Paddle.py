'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         This file is created to load the paddles for the players. The key inputs
                 from the players are accepted and determines where their paddles will go.
                 This file contains code which prevents the paddle from going out of bounds.
                 It also contains code to get the angle of the paddle in relation to the
                 coordinate plane and use it when the paddle collides with the puck to determine
                 bounces appropriately. Lastly, the code in this file detects whether the
                 paddle has collided with the puck.
'''

# Imports pygame and math modules to invoke their functions
import pygame, math
# Imports all local functions from pygame.local 
from pygame.locals import *
# Initiates pygame
pygame.init()

# Controls that the players are going use to control the movement of the paddle
controls = [[K_UP, K_DOWN, K_LEFT, K_RIGHT], [K_w, K_s, K_a, K_d]]

class Paddle(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to output the paddles for the players to the screen and
                set the barriers for the paddles. It allows the paddles' velocity and location
                to be updated in response to the players' keyboard inputs. It allows the angle of
                the paddles in relation to the coordinate plane to be retrieved which is used
                when the paddles collide with the puck. It also allows for paddle and puck collisions
                to be detected.
    '''

    def __init__(self, img, id, top, left, bottom, right, size):
        '''
        Parameter: <img> is a string of the filename that contains the image for the paddles
                   <id> is an integer that represents the paddle player number
                   <top> is an integer that represents the top barrier of the paddles
                   <left> is an integer that represents the left barrier of the paddles
                   <bottom> is an integer that represents the bottom barrier of the paddles
                   <right> is an integer that represents the right barrier of the paddles
                   <size> is an integer that represents the size of the paddles
        Return:    Returns the paddle object (allows the players to see their paddles)
        Purpose:   This method is created to output the paddles of players to the screen according
                   to their keyboard inputs. This method also determines the attributes of the paddles
                   (barrier and velocity in x and y direction).
        '''
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Size of the image
        self.image = pygame.Surface((size, size))
        # Makes the paddle a specific size and loads image of the paddle to the surface
        pygame.transform.scale(pygame.image.load(img).convert_alpha(), (size, size), self.image)
        # Makes the background of the paddle transparent
        self.image.set_colorkey(self.image.get_at((0,0)))
        # Determines the attributes of the paddle
        self.rect = self.image.get_rect()
        # Determines the midpoint of the area that the paddle can move (starting point)
        self.rect.topleft = (((left+right)/2)-size/2), (((top+bottom)/2)-size/2)
        # Decides which set of controls is used
        self.id = id

        # Determines attributes of the paddle (barrier and velocity in x and y direction)
        self.xmin = left
        self.ymin = top
        self.xmax = right
        self.ymax = bottom
        self.vx = 0
        self.vy = 0

    def update(self, keys):
        '''
        Parameters: <keys> is a dictionary; states of all the keys
        Return:     None
        Purpose:    This method is created to respond to the keyboard inputs from the user.
                    It updates the direction and velocity that the paddle will travel in
                    according to keyboard inputs. Also, this method will prevent the paddle
                    from moving in its direction once it hits the barrier. Once the paddle
                    hits a barrier there will be a distinctive collision sound.
        '''

        # Accelerates the paddle if key is pressed
        # If up key or key 'w' is pressed depending on the index
        if keys[controls[self.id][0]]:
            # Paddle goes up
            self.vy -= 1.2
        # If down key or key 's' is pressed depending on the index
        if keys[controls[self.id][1]]:
            # Paddle goes down
            self.vy += 1.2
        # If left key or key 'a' is pressed depending on the index
        if keys[controls[self.id][2]]:
            # Paddle goes left
            self.vx -= 1.2
        # If right key or key 'd' is pressed depending on the index
        if keys[controls[self.id][3]]:
            # Paddle goes right
            self.vx += 1.2

        # Decelerates the paddle
        # If moving forward (horizontally)
        if self.vx>0:
            self.vx -= 0.5
        # If moving backward (horizontally)
        elif self.vx<0:
            self.vx += 0.5
        # If moving down (vertically)
        if self.vy>0:
            self.vy -= 0.5
        # If moving up (vertically)
        elif self.vy<0:
            self.vy += 0.5

        # Controls the speed of the paddle so that it cannot be greater than a certain amount
        self.vx = min(self.vx, 20)
        self.vy = min(self.vy, 20)

        # Moves the paddles' rect
        self.rect.move_ip(self.vx, self.vy)

        # Forms the barrier in which the paddle can move
        # If paddle hits the left barrier
        if self.rect.left<self.xmin:
            # Forms left barrier for each paddle
            self.rect.left = self.xmin

            # If the red paddle hits the left barrier (blue paddle's left barrer is the middle the air hockey table which is not "wood")
            if self.id == 1:
                # Plays distinctive collision sound when the paddle hits the barrier
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # When paddle hits the left barrier it stops moving
            self.vx = 0
        # If paddle hits the right barrier
        elif self.rect.right>self.xmax:
            # Forms right barrier for each paddle
            self.rect.right = self.xmax

            # If the blue paddle hits the right barrier (red paddle's right barrer is the middle the air hockey table which is not "wood")
            if self.id == 0:
                # Plays distinctive collision sound when the paddle hits the barrier
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # When paddle hits the right barrier it stops moving
            self.vx = 0

        # If paddle hits the top barrier
        if self.rect.top<self.ymin:
            # Forms the top barrier for each paddle
            self.rect.top = self.ymin

            # Plays distinctive collision sound when the paddle hits the barrier
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # When paddle hits the top barrier its stops moving
            self.vy = 0
        # If paddle hits the bottom barrier
        elif self.rect.bottom>self.ymax:
            # Forms the bottom barrier for each paddle
            self.rect.bottom = self.ymax

            # Plays distinctive collision sound when the paddle hits the barrier
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # When paddle hits the bottom barrier it stops moving
            self.vy = 0

    def getAngle(self):
        '''
        Parameters: None
        Return:     Angle of paddle (math.atan2(-self.vy, self.vx))
        Purpose:    Calculates the current angle of the paddle to be used when the puck
                    collides with the paddle
        '''

        # Calculates the current angle of paddle in relation to the coordinate plane and returns it
        # to be used when the puck collides with the paddle
        return math.atan2(-self.vy, self.vx)

    def collide(self, puck):
        '''
        Parameters: <puck> is a puck object
        Return:     True if the paddle collides with the puck, False otherwise
        Purpose:    Checks if the paddle collides with the puck by determining the distance
                    between the puck and paddle
        '''

        # Determines coordinates of the centre of the puck and paddles
        paddlex = self.rect.centerx
        paddley = self.rect.centery
        puckx = puck.rect.centerx
        pucky = puck.rect.centery

        # Using the coordinates of the centre of the puck and paddles to determine the distance
        # between the puck and paddles. The distance is to determine if the puck and paddle have collided
        dist = ((paddlex-puckx)**2+(paddley-pucky)**2)**0.5
        # Radius of paddle
        paddleradius = (self.rect.width)/2
        # Radius of puck
        puckradius = (puck.rect.width)/2

        # If the distance betweeen the puck and paddle is less than the sum of the radius of the paddle and the radius of the puck they have collided
        if (dist<=paddleradius+puckradius-1):
            # A distinctive collision sound between the puck and paddle will be played
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("collision.wav"))
            # There is a collision
            return True
        else:
            # There is no collision
            return False
