'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         This file is created to create the base of the goal to detect
                 whether the puck has entered the goal and a goal has been scored.
'''

# Imports the pygame module to invoke its functions
import pygame
# Imports all local functions from pygame.local
from pygame.locals import *

class GoalSideBlock(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to create a block on each side of the left
                and right goals. This forms the barrier for the puck and paddles.
    '''

    def __init__(self, id, left, top, width):

        '''
        Parameter: <id> is an integer that represents the either the upper left side block, lower left side block,
                        upper right side block, or lower right side block
                   <left> is an integer that represents the left (y) coordinate position of the goalSideBlocks
                   <top> is an integer that represents the top (x) coordinate position of the goalSideBlocks
                   <width> is an integer that represents the size of the goalSideBlocks
        Return:    None
        Purpose:   This method is created to create the goalSideBlocks.
        '''
        
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Creates a goalSideBlock
        self.image = pygame.Surface((55, width)).convert()
        # Colour of goalSideBlock is brown
        self.image.fill((138, 54, 15))
        # Determines the attributes of the goal as a rectangle
        self.rect = self.image.get_rect()

        # Sets the position of the goal
        self.rect.left = left
        self.rect.top = top
