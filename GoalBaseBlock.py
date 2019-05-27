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

class GoalBaseBlock(pygame.sprite.Sprite):

    '''
    Parameters: None
    Return:     None
    Purpose:    This class is created to create a block to detect whether the puck has
                entered the goal. The block is narrow enough so that the entire puck can
                enter the goal before a goal is scored.
    '''

    def __init__(self, id, lt, tp, width):

        '''
        Parameter: <id> is an integer that represents the either the left or right goalBaseBlock
                   <lt> is an integer that represents the left (y) coordinate position of the goalBaseBlock
                   <tp> is an integer that represents the top (x) coordinate position of the goalBaseBlock
                   <width> is an integer that represents the size of the goalBaseBlock
        Return:    None
        Purpose:   This method is created to create the goalBaseBlock to detect whether a goal is scored.
        '''
        
        # Constructs the parent component
        pygame.sprite.Sprite.__init__(self)
        # Creates a goal
        self.image = pygame.Surface((11,width)).convert()
        # Colour of goal is black
        self.image.fill((0,0,0))
        # Determines the attributes of the goal as a rectangle
        self.rect = self.image.get_rect()

        # Sets the position of the goalBaseBlock
        self.lt = lt
        self.tp = tp

        # Sets the size of the goalBaseBlock
        self.width = width

    def get_rect(self):

        '''
        Parameter: None
        Return:    The rectangle coordinates of the goalBaseBlock
        Purpose:   This method is created to return the rectangle coordinates of the goalBaseBlock. The
                   coordinates are used to detect whether a goal has been scored (when the puck collides
                   with the goalBaseBlock)
        '''

        # Returns the rectangle coordinates of the goalBaseBlock
        return pygame.Rect(self.lt, self.tp, 11, self.width)
