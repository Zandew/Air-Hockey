'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         This file is created to create the left and right goals on the
                 air hockey table.
'''

# Imports the pygame module to invoke its functions
import pygame
# Imports all local functions from pygame.local
from pygame.locals import *

class Goal(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to create the left and right goals on the
                air hockey table.
    '''

    def __init__(self, id, left, top, width):

        '''
        Parameter: <id> is an integer that represents the either the left or right goal
                   <left> is an integer that represents the left (y) coordinate position of the goal
                   <top> is an integer that represents the top (x) coordinate position of the goal
                   <width> is an integer that represents the size of the goal
        Return:    None
        Purpose:   This method is created to create the left and right goals on the air hockey table.
        '''
        
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Creates a goal
        self.image = pygame.Surface((55,width)).convert()
        # Colour of goal is black
        self.image.fill((0,0,0))
        # Determines the attributes of the goal as a rectangle
        self.rect = self.image.get_rect()

        # Sets the position of the goal
        self.rect.left = left
        self.rect.top = top
