"""
File: Alien
Author: Chavi Parks
Description: A class to represent a single alien in a fleet.
"""
import pygame

from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):
        """initialize the alien and set its starting position."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the alien imae and set its rect attribute.
        self.image = pygame.image.load("images/Crow.bmp")
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        """The 'x' and 'y' are the location on the screen, while the
        'width' and 'height' represent the actual aliens height and width
        defined by its rect.
        """
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal posoition
        self.x = float(self.rect.x)


    def update(self):
        """Move the Alien to the right."""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        






        
