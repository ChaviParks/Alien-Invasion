"""
File: Alien Invasion
Author: Chavi Parks 
Decsription: *See alien invasion description document*
"""

import sys
from time import sleep

import pygame

from settings import MySettings
from game_stats import GameStats
from scoreboard import ScoreBoard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    """Overall Class to manage game assets and behaviors."""

    def __init__(self):
        "initialize the game, and create game resources."""
        pygame.init()
        self.settings = MySettings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        """Code to put the game in full screen. Uncomment to test code."""
##        self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
##        self.settings.screen_width = self.screen.get_rect().width
##        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion!")

        #Create an instance to store game statistics
        #and socreboard
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        #Make a play button.
        self.play_button = Button(self,"Play")
        
        self.ship = Ship(self)
        
        #Create a group to store all the live bullets 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Check to see if a highscore already exists.
        

        

        




    def run_game(self):
        """Start main loop for the game"""
        
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()

            
           
         
      
    def _check_events(self):
        
           #respond to keypresses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # quits pygame
                sys.exit()
         
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()
        
                    
                    
                        
    def _check_keydown_events(self, event):
        #Respondes to key presses
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        



    def _check_keyup_events(self, event):
        #Respondes to key releases
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    

    def _start_game(self):
        
        """Starts a new game when conditions are met."""
        #Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        #Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        #Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    
    def _update_screen(self):
        
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        if not self.stats.game_active:
            self.play_button.draw_button()
            
        else:
            self.sb.show_score()
            self.ship.blitme()

            #Draws the bullets on the screen
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)
        

        #Make the most recently drawn screen visible
        pygame.display.flip()




    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        #Update bullet position
        self.bullets.update()

        #Get rid of bullets that have dissapered.
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

   

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien colisions."""
        #Remove any bullets and aliens that have collieded.
        
        collisions = pygame.sprite.groupcollide(
                self.bullets , self.aliens, True, True)

        if collisions:
            #Loop through values in collision dict to award points
            #for each alien.
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Destroy existing bullets aNd create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increease level
            self.stats.level += 1
            self.sb.prep_level()
        

    def _update_aliens(self):
        """Check if the fleet is at an aedge,
         Then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
        


    def _fire_bullets(self):
        """Create a bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determin the number of rows of aliens that fit on screen.
        ship_height = self.ship.rect.height
        
        available_space_y = (self.settings.screen_height -
                                 (3 * alien_height) - ship_height)
        
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens.
        for row_number in range (number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriatly if any  aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            

            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            #Pause.
            sleep(0.6)
            
        else:
            self._save_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        
           

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _save_score(self):

        HS = open("MyHighScore.txt","w")
        HS.write(str(self.stats.high_score))
        HS.close()

        
        
     
        

    

        
        



        


if __name__== '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()