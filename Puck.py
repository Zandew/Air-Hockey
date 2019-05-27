'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         This puck file is created to load the puck to the screen. Also the barriers for
                 the puck are set to ensure the puck does not go out of bounds. The location of
                 the puck is updated depending on collisions with the paddles and barriers. Due to
                 collisions with the paddles the angle and speed in which the puck travels in will
                 change.
'''

# Modules are imported to invoke their functions
import pygame, math, random
# Imports all local functions from pygame.local 
from pygame.locals import *

def getAngle(x1, y1, x2, y2):

    '''
    Parameter: <x1> is an integer that represents the x-coordinate of the first point
               <y1> is an integer that represents the y-coordinate of the first point
               <x2> is an integer that represents the x-coordinate of the second point
               <y2> is an integer that represents the y-coordinate of the second point
    Return:    Returns the angle between 2 points
    Purpose:   This function is created to calculate and return the angle between 2 points
    '''

    # Difference between y values
    yv = y2-y1
    # Difference between x values
    xv = x1-x2

    # Determines how the puck should bounce off the paddle if difference in x values is 0
    if xv == 0:
        # If difference in y values is less than 0
        if yv < 0:
            return math.pi/2
        # If difference in y values is greater than or equal to 0
        else:
            return 3/2*math.pi

    # Returns the angle between 2 points
    return math.atan2(yv, xv)

def calibrate(angle):

    '''
    Parameter: <angle> is an integer that represents the angle between the puck and paddle
    Return:    Returns the angle between 0 and 2 pi
    Purpose:   This function is created to calibrate the angle so that it is between 0 and 2 pi
    '''

    # Takes the angle between the puck and paddle and returns the angle so that it is between 0
    # and 2 pi(in radians); thus it returns the angle so that it is between 0 and 360 degrees
    while (angle<0):
        angle += math.pi*2
    while (angle>=math.pi*2):
        angle -= math.pi*2
    return angle

def minDist(angle1, angle2):

    '''
    Parameter: <angle1> is an integer that represents the first angle
               <angle2> is an integer that represents the second angle
    Return:    Returns the minimum angle between the 2 angles
    Purpose:   This function is created to calculate and return the minimum angle between 2 angles
    '''

    # Calculates and returns the minimum angle between 2 angles
    return min(calibrate(angle1-angle2), calibrate(angle2-angle1))

class Puck(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to load the puck to the screen. Also the barriers for
                the puck are set to ensure the puck does not go out of bounds. The location of
                the puck is updated depending on collisions with the paddles and barriers. Due to
                collisions with the paddles the angle and speed in which the puck travels in will
                change.
    '''

    def __init__(self, img, top, left, bottom, right, size):

        '''
        Parameter: <img> is a string of the filename that contains the image for the puck
                   <top> is an integer that represents the top barrier of the puck
                   <left> is an integer that represents the left barrier of the puck
                   <bottom> is an integer that represents the bottom barrier of the puck
                   <right> is an integer that represents the right barrier of the puck
                   <size> is an integer that represents the size of the puck
        Return:    Returns the puck object (allows the players to see the puck)
        Purpose:   This method is created to output the puck to the screen. This method also
                   determines the attributes of the paddles (barrier and velocity in x and y
                   direction).
        '''
        
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Size of the image
        self.image = pygame.Surface((size,size))
        # Makes the puck a specific size and loads image of the puck to the surface
        pygame.transform.scale(pygame.image.load(img).convert_alpha(), (size,size), self.image)
        # Makes the background of the puck transparent
        self.image.set_colorkey(self.image.get_at((0,0)))
        # Determines the attributes of the puck
        self.rect = self.image.get_rect()
        # Determines the midpoint of the area that the paddle can move (starting point)
        self.rect.topleft = (((left+right)/2)-size/2, ((top+bottom)/2)-size/2)

        # Determines attributes of the paddle (barrier and speed)
        self.xmin = left
        self.ymin = top
        self.xmax = right
        self.ymax = bottom
        self.angle = 0
        self.speed = 0

    def update(self):
        
        '''
        Parameter: None
        Return:    None
        Purpose:   This method is created to update the location of the puck. It prevents the puck
                   from going out of bounds and plays a distinctive collision sound if the puck
                   collides with the barrier. If the speed of the puck is greater than a certain
                   speed it will decelerate.
        '''

        # Puck decelerates if it is greater than a certain speed
        if (self.speed>0.2):
            self.speed -= 0.2
        # If the puck is less than a certain speed it will stop
        else:
            self.speed = 0

        # Moves the puck's rect
        self.rect.move_ip(math.cos(self.angle)*self.speed, -math.sin(self.angle)*self.speed)

        # Determines the angle between the puck and paddle
        self.angle = calibrate(self.angle)

        # If the puck hits the left barrier
        if self.rect.left<self.xmin:
            # Forms left barrier for puck
            self.rect.left = self.xmin

            # A distinctive collision sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # Determines the angle at which the puck should bounce off the wall
            # Using Python's mathematical functions the puck is programmed to bounce off the boundary
            # in a specific way depending on how it collides with the boundary
            if (self.angle<math.pi):
                self.angle = math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle-math.pi

        # If the puck hits the right barrier
        elif self.rect.right>self.xmax:
            # Forms right barrier for puck
            self.rect.right = self.xmax

            # A distinctive collision sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # Determines the angle at which the puck should bounce off the wall
            # Using Python's mathematical functions the puck is programmed to bounce off the boundary
            # in a specific way depending on how it collides with the boundary
            if (self.angle<math.pi/2):
                self.angle = math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle+math.pi

        # If the puck hits the top barrier
        if self.rect.top<self.ymin:
            # Forms top barrier for puck
            self.rect.top = self.ymin

            # A distinctive collision sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # Determines the angle at which the puck should bounce off the wall
            # Using Python's mathematical functions the puck is programmed to bounce off the boundary
            # in a specific way depending on how it collides with the boundary
            if (self.angle<math.pi/2):
                self.angle = math.pi*2-self.angle
            else:
                self.angle = math.pi-self.angle+math.pi

        # If the puck hits the bottom barrier
        elif self.rect.bottom>self.ymax:
            # Forms bottom barrier for puck
            self.rect.bottom = self.ymax

            # A distinctive collision sound is played
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))

            # Determines the angle at which the puck should bounce off the wall
            # Using Python's mathematical functions the puck is programmed to bounce off the boundary
            # in a specific way depending on how it collides with the boundary
            if (self.angle<3/2*math.pi):
                self.angle = 2*math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle

        # Moves the puck's rect while it is colliding with a barrier
        while (self.rect.left<self.xmin or self.rect.right>self.xmax or self.rect.top<self.ymin or self.rect.bottom>self.ymax):
            self.rect.move_ip(math.cos(self.angle)*self.speed, -math.sin(self.angle)*self.speed)

    def bounce(self, paddle):

        '''
        Parameter: <paddle> is an object that collides with the puck
        Return:    None
        Purpose:   This method is created to change the puck's angle and speed as a result of the collision with the paddle.
        '''

        # Determines the coordinates of the centre of the paddle
        paddlex = (paddle.rect.left+paddle.rect.right)/2
        paddley = (paddle.rect.top+paddle.rect.bottom)/2

        # Determines the coordinates of the centre of the puck
        puckx = (self.rect.left+self.rect.right)/2
        pucky = (self.rect.top+self.rect.bottom)/2

        # Determines the angle between the puck and paddle
        angle = calibrate(getAngle(puckx, pucky, paddlex, paddley))

        # Determines different angles between the puck and paddle used for collisions
        reflect_angle = calibrate(angle-math.pi/2)
        opp_angle = calibrate(angle+math.pi/2)
        self.angle = calibrate(self.angle)

        # Determines the current angle of the paddle; used when the paddle collides with the puck 
        paddle_angle = paddle.getAngle()

        # If the speed of the puck is 0 (not moving) the angle the puck will move is the angle between the puck and paddle 
        if (self.speed==0):
            self.angle = angle
        elif ((paddle.vx!=0 or paddle.vy!=0) and minDist(self.angle, calibrate(paddle_angle))<math.pi/2):
            num = math.sin(self.angle)*self.speed-paddle.vy
            den = math.cos(self.angle)*self.speed+paddle.vx
            self.angle = math.atan2(num, den)
        else:
            d1 = minDist(self.angle, reflect_angle)
            d2 = minDist(self.angle, opp_angle)
            if (d1<d2):
                if (self.angle==calibrate(reflect_angle+d1)):
                    self.angle = reflect_angle-d1
                else:
                    self.angle = reflect_angle+d1
            else:
                if (self.angle==calibrate(opp_angle+d2)):
                    self.angle = opp_angle-d2
                else:
                    self.angle = opp_angle+d2
        self.speed += (paddle.vx**2+paddle.vy**2)**0.5
        self.speed = min(self.speed, 25)
        while (paddle.collide(self)):
            x = -math.cos(angle)
            if (x>0):
                x += 1
            elif (x<0):
                x -= 1
            y = math.sin(angle)
            if (y>0):
                y += 1
            elif (y<0):
                y -= 1
            paddle.rect.move_ip(round(x, 2), round(y, 2))
