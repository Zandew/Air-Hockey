import pygame
import math
from pygame.locals import *

import random

def getAngle(x1, y1, x2, y2):
    '''
    Calculates the angle between 2 points
    Parameters:
        x1, y1, x2, y2 (int): x and y values of 2 points
    Returns: angle between 2 points
    '''
    yv = y2-y1
    xv = x1-x2
    if (xv==0):
        if (yv<0):
            return math.pi/2
        else:
            return 3/2*math.pi
    return math.atan2(yv, xv)

def calibrate(angle):
    '''
    Calibrates angle so that it is between 0 and 2pi
    Paramters:
        angle (int): the angle
    Returns: Angle between 0 and 2pi
    '''
    while (angle<0):
        angle += math.pi*2
    while (angle>=math.pi*2):
        angle -= math.pi*2
    return angle

def minDist(angle1, angle2):
    '''
    Calculates minimum angle between 2 angles
    Parameters:
        angle1, angle2 (int): the 2 angles
    Returns: minimum angle between 2 angles
    '''
    return min(calibrate(angle1-angle2), calibrate(angle2-angle1))

class Puck(pygame.sprite.Sprite):

    '''
    Puck class for hockey puck

    Attributes:
        img (str): file that contains puck image
        top, left, bottom, right (int): boundaries of the puck
        size (int): size of puck

    Methods:
        update()
        bounce(paddle)
    '''

    def __init__(self, img, top, left, bottom, right, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size,size))
        pygame.transform.scale(pygame.image.load(img).convert_alpha(), (size,size), self.image)
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (((left+right)/2)-size/2, ((top+bottom)/2)-size/2)
        self.xmin = left
        self.ymin = top
        self.xmax = right
        self.ymax = bottom
        self.angle = 0
        self.speed = 0

    def update(self):
        '''
        Updates the location of puck

        Returns: None
        '''
        if (self.speed>0.2):
            self.speed -= 0.2
        else:
            self.speed = 0
        self.rect.move_ip(math.cos(self.angle)*self.speed, -math.sin(self.angle)*self.speed)
        self.angle = calibrate(self.angle)
        if self.rect.left<self.xmin:
            self.rect.left = self.xmin
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))
            '''
            wallSound = pygame.mixer.Sound("wall.wav")
            wallSound.play()
            '''
            if (self.angle<math.pi):
                self.angle = math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle-math.pi
        elif self.rect.right>self.xmax:
            self.rect.right = self.xmax
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))
            '''
            wallSound = pygame.mixer.Sound("wall.wav")
            wallSound.play()
            '''
            if (self.angle<math.pi/2):
                self.angle = math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle+math.pi
        if self.rect.top<self.ymin:
            self.rect.top = self.ymin
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))
            '''
            wallSound = pygame.mixer.Sound("wall.wav")
            wallSound.play()
            '''
            if (self.angle<math.pi/2):
                self.angle = math.pi*2-self.angle
            else:
                self.angle = math.pi-self.angle+math.pi
        elif self.rect.bottom>self.ymax:
            self.rect.bottom = self.ymax
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wall.wav"))
            '''
            wallSound = pygame.mixer.Sound("wall.wav")
            wallSound.play()
            '''
            if (self.angle<3/2*math.pi):
                self.angle = 2*math.pi-self.angle
            else:
                self.angle = math.pi*2-self.angle
        while (self.rect.left<self.xmin or self.rect.right>self.xmax or self.rect.top<self.ymin or self.rect.bottom>self.ymax):
            self.rect.move_ip(math.cos(self.angle)*self.speed, -math.sin(self.angle)*self.speed)

    def bounce(self, paddle):
        '''
        Changes the puck's angle and speed due to collision with paddle

        Parameters:
            paddle (paddle): the paddle that puck collides with

        Returns: None
        '''
        paddlex = (paddle.rect.left+paddle.rect.right)/2
        paddley = (paddle.rect.top+paddle.rect.bottom)/2
        puckx = (self.rect.left+self.rect.right)/2
        pucky = (self.rect.top+self.rect.bottom)/2
        angle = calibrate(getAngle(puckx, pucky, paddlex, paddley))
        reflect_angle = calibrate(angle-math.pi/2)
        opp_angle = calibrate(angle+math.pi/2)
        self.angle = calibrate(self.angle)
        paddle_angle = paddle.getAngle()
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
