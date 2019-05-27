'''
Programmed by:   Albert Chan and Andrew Xue
Programmed on:   May 26, 2019
Programmed for:  ICS3U1-04
Purpose:         This file is created to create a block on each side of the left
                 and right goals. This forms the barrier for the puck and paddles
                 and prevents them from going out of bounds.
'''

# Imports the pygame module to invoke its functions
import pygame
# Imports all local functions from pygame.local
from pygame.locals import *

class GoalSideBounceBlock(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to create a block on each side of the left
                and right goals. This forms the barrier for the puck and paddles
                and prevents them from going out of bounds.
    '''

    def __init__(self, id, lt, tp, width):

        '''
        Parameter: <id> is an integer that represents the either the left or right goalBaseBlock
                   <lt> is an integer that represents the left (y) coordinate position of the goalBaseBlock
                   <tp> is an integer that represents the top (x) coordinate position of the goalBaseBlock
                   <width> is an integer that represents the size of the goalBaseBlock
        Return:    None
        Purpose:   This method is created to create the goalSideBounceBlock to detect whether a goal is scored.
        '''
        
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Creates a goalSideBounceBlock
        self.image = pygame.Surface((55,width)).convert()
        # Colour of goalSideBounceBlock is brown
        self.image.fill((138, 54, 15))
        # Determines the attributes of the goal as a rectangle
        self.rect = self.image.get_rect()

        # Sets the position of the goal
        self.lt = lt
        self.tp = tp

        # Sets the size of the goalSideBounceBlock
        self.width = width

    def get_rect(self):

        '''
        Parameter: None
        Return:    The rectangle coordinates of the goalBaseBlock
        Purpose:   This method is created to return the rectangular coordinates of the goalSideBounceBlock. The
                   coordinates are used to detect whether the puck or paddles have collided with the barrier. This
                   prevents the puck and paddles from going out of bounds.
        '''

        # Returns the rectangular coordinates of the goalSieBounceBlock
        return pygame.Rect(self.lt, self.tp, 55, self.width)
