"""
File: Ship
Author: Chavi Parks
Description: A class to manage the ship in Alien Invasion
"""
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game):
        """initialize the ship and set its starting position."""
        super().__init__()
        
        self.screen = ai_game.screen
        self.setting = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/Farmer.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        #Movement flag in order to create continuous Movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the Movement Flag."""
        #Update the ship's x value, not the rect.
        
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
            
        if self.moving_left and self.rect.left > 0 :
            self.x -= self.setting.ship_speed
            
        self.rect.x = self.x

    def blitme(self):
        """Draw the  ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


        
        
