"""
File: Game Stats
Author: Chavi Parks
Description: A class for tracking statistics for Alien Invasion
"""


class GameStats:

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        #Start AI in an inactive state.
        self.game_active = False

        try:
            HS = open("MyHighScore.txt","r")
            HS = HS.readline()
            self.high_score = int(HS)
            
        except FileNotFoundError:
           
            self.high_score = 0


    def reset_stats(self):
        """Initialize statistics that can change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
