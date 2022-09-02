"""
File: Settings
Author: Chavi Parks
Description: A class of my settings class, to modify settings in one,
easy to find location.
"""

class MySettings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """initialize the  game's static settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        #sets background color
        self.bg_color = (0,195,239)

        #ships settings
        self.ship_limit = 3
       
        #Bullet settings
        self.bullet_width = 4
        self.bullet_height = 9
        self.bullet_color = (30,30,30)
        self.bullets_allowed = 6

        #Alien settings
        self.fleet_drop_speed = 10
      
        #How quickly the game speeds up
        self.speedup_scale = 1.2

        #How quickly the alien points value increse
        self.score_scale = 1.5

        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.0
        self.bullet_speed = 1.5
        self.alien_speed = 0.5

        #Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #Scoring
        self.alien_points = 25

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


        self.alien_points = int(self.alien_points * self.score_scale)
        



        
        
