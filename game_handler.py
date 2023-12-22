
import pygame
import sys
import random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from src.UI.Buttons import Button
from src.enemys.enemy import Enemy
from src.player.scoring import ScoringHandler
from src.player.player import Player


pygame.init()
pygame.mixer.init()




class Game:
    def __init__(self):
        self.game_score:int

        #game sound
        self.mute_sound = False
        self.game_over_sound = pygame.mixer.Sound("./assets/music/game_over.mp3")
        self.game_sound = pygame.mixer.Sound("./assets/music/game.mp3")
        self.menu_sound = pygame.mixer.Sound("./assets/music/main_screen.mp3")

        # display dimensions
        self.display_width = 800
        self.display_height = 800
        # game variables
        # grid size
        self.tile_size = 40
        # display sizes
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.clock = pygame.time.Clock()
        # background image
        self.background = pygame.image.load("./assets/images/world/BG.png")
        # player settings
        self.player = Player(pos_x=self.tile_size*3, pos_y=self.tile_size*18.5, width=40, height=40, speed=5)
        # enemy setting
        self.enemy = Enemy(random.randint(0, self.display_width-40), random.randint(0, self.display_height-40), width=40, height=40, speed=2)
        self.scoringHandler = ScoringHandler()
        # for game over event
        self.game_over_font = pygame.font.SysFont(None, 80)
        self.game_over_font_text = pygame.font.SysFont(None, 50)
        self.game_over_font_text_score = pygame.font.SysFont(None, 30)
        # screen name
        pygame.display.set_caption("SAND")
        self.go = True
        # asset images
        grass_img = pygame.image.load("./assets/images/StoneBlock.png")
        dirt_img = pygame.image.load("./assets/images/Stone.png")    
        # placeholder for assets (map)
        self.tile_list = []
        row_count = 0
        # map structure
        self.world_data = [
            [2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2],
            [2	,0	,0	,0	,0	,0	,0	,0	,0	,0	,2	,0	,0	,2	,0	,0	,0	,0	,0	,2],
            [2	,0	,0	,0	,2	,2	,2	,2	,2	,0	,2	,0	,0	,2	,0	,0	,0	,0	,0	,2],
            [2	,2	,0	,0	,0	,0	,0	,2	,2	,0	,2	,0	,0	,2	,0	,0	,2	,0	,0	,2],
            [2	,0	,0	,0	,0	,0	,0	,2	,2	,0	,2	,0	,0	,2	,0	,0	,2	,0	,0	,2],
            [2	,0	,0	,0	,0	,0	,0	,2	,2	,0	,0	,0	,0	,0	,0	,0	,2	,0	,2	,2],
            [2	,2	,2	,2	,0	,0	,0	,0	,2	,0	,0	,0	,0	,0	,0	,0	,2	,0	,0	,2],
            [2	,0	,2	,0	,0	,0	,0	,0	,2	,2	,2	,0	,2	,2	,2	,0	,2	,0	,0	,2],
            [2	,0	,2	,0	,0	,0	,0	,0	,2	,0	,0	,0	,0	,2	,0	,0	,2	,0	,0	,2],
            [2	,0	,2	,0	,0	,0	,0	,2	,2	,0	,0	,0	,0	,2	,0	,0	,2	,0	,2	,2],
            [2	,0	,0	,0	,2	,0	,0	,0	,2	,0	,0	,0	,0	,2	,0	,0	,2	,0	,0	,2],
            [2	,0	,0	,0	,2	,0	,0	,0	,2	,0	,2	,0	,0	,0	,0	,0	,2	,0	,0	,2],
            [2	,0	,0	,0	,2	,0	,0	,0	,2	,0	,2	,0	,0	,0	,0	,0	,2	,0	,0	,2],
            [2	,0	,0	,0	,2	,2	,0	,0	,0	,0	,2	,2	,2	,2	,2	,0	,2	,2	,0	,2],
            [2	,0	,2	,2	,2	,0	,0	,2	,0	,0	,2	,0	,0	,0	,0	,0	,0	,2	,0	,2],
            [2	,0	,2	,0	,2	,0	,0	,2	,0	,0	,2	,0	,0	,0	,0	,0	,0	,0	,0	,2],
            [2	,0	,2	,0	,2	,0	,0	,2	,2	,2	,2	,0	,2	,2	,2	,0	,0	,0	,0	,2],
            [2	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,2	,0	,2],
            [2	,0	,0	,0	,2	,0	,0	,2	,0	,0	,0	,0	,0	,0	,0	,0	,0	,2	,0	,2],
            [2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2	,2]
            ]
        # mapping the the images to the playground
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    # format the image based on the tile_size
                    img = pygame.transform.scale(dirt_img, (self.tile_size, self.tile_size))
                    # create rect-object
                    img_rect = img.get_rect()   
                    # x-pos
                    img_rect.x = col_count * self.tile_size
                    # y-pos
                    img_rect.y = row_count * self.tile_size
                    # Assignment of img and pos
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
        # enemy list
        self.enemy_list = [self.enemy]
        # game started variable
        self.game_started = False
        # game closed variable
        self.game_exit = False
    
    # GRID FOR TESTING
    #def draw_grid(self):
    #    for line in range(0, 20):
    #        pygame.draw.line(self.screen, (255, 255, 255), (0, line * self.tile_size), (self.display_width, line * self.tile_size))
    #        pygame.draw.line(self.screen, (255, 255, 255), (line * self.tile_size, 0), (line * self.tile_size, self.display_height))

    # display tile on screen
    def draw(self):
        # display each tile from the list on the screen
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])


    def show_game_over(self):
        # get the score
        # self.score_text = self.scoring()
        # test
        self.score_text = self.game_score
        
        # format to surface
        game_over_score_text = self.game_over_font.render(f"Your Score:", True, (255, 0, 0))
        game_over_score_text_points = self.game_over_font.render(f"{self.score_text}", True, (255, 0, 0))
        game_over_text = self.game_over_font.render("Game Over", True, (255, 0, 0))
        restart_text = self.game_over_font.render("Press 'R' to play again", True, (255, 0, 0))
        close_text = self.game_over_font.render("Press 'C' to close", True, (255, 0, 0))
        # rendering the event text
        # game_over_score_text
        self.screen.blit(game_over_score_text, (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 2 - game_over_text.get_height() // 2 - 30))
        # game_over_score_text_points
        self.screen.blit(game_over_score_text_points, (self.display_width // 2 - game_over_text.get_width() // 6, self.display_height // 2 - game_over_text.get_height() // 2 +40))
        # game_over_text
        self.screen.blit(game_over_text, (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 2 - game_over_text.get_height() // 2 - 150))
        # restart_text
        self.screen.blit(restart_text, (self.display_width // 2 - restart_text.get_width() // 2, self.display_height // 2 + game_over_text.get_height() // 2 + 160))
        # close_text
        self.screen.blit(close_text, (self.display_width // 2 - close_text.get_width() // 2, self.display_height // 2 + game_over_text.get_height() // 2 + 230))
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                # check for closing the game via cross
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            # check for input "r" to restart the game
            if keys[pygame.K_r]:
                self.reset_game()
                waiting_for_input = False

            # close the game if the player press "c"                
            elif keys[pygame.K_c]:
                pygame.quit()
                sys.exit()


    # check the collision between player and enemy
    def check_collision(self):

        # player collision between enemies
        if self.player.pos_x < self.enemy.pos_x + self.enemy.width and self.player.pos_x + self.player.width > self.enemy.pos_x:
            if self.player.pos_y < self.enemy.pos_y + self.enemy.height and self.player.pos_y + self.player.height > self.enemy.pos_y:
                return True

        # player collision
        player_rect = pygame.Rect(self.player.pos_x, self.player.pos_y, self.player.width, self.player.height)
        # check if the rectangle of the player overlaps with the rectangle of the block
        for tile in self.tile_list:
            tile_rect = tile[1]
            if player_rect.colliderect(tile_rect):
                # Check if the player is standing on a block from above
                if player_rect.bottom > tile_rect.top and self.player.pos_y  < tile_rect.top:
                    self.player.pos_y = tile_rect.top - self.player.height

                # Check if the player bumps into a block from below
                # checked that the bottom edge of the player is below the bottom edge of the block
                elif player_rect.top < tile_rect.bottom and self.player.pos_y + self.player.height > tile_rect.bottom:
                    self.player.pos_y = tile_rect.bottom
                # Checking if the player bumps into a block from the right
                elif player_rect.right > tile_rect.left and self.player.pos_x < tile_rect.left:
                    self.player.pos_x = tile_rect.left - self.player.width
                # Check if the player bumps into a block from the left
                elif player_rect.left < tile_rect.right and self.player.pos_x + self.player.width > tile_rect.right:
                    self.player.pos_x = tile_rect.right

        # enemy collision
        enemy_rect = pygame.Rect(self.enemy.pos_x, self.enemy.pos_y, self.enemy.width, self.enemy.height)
        # check if the rectangle of the enemy overlaps with the rectangle of the block
        for tile in self.tile_list:
            tile_rect = tile[1]
            if enemy_rect.colliderect(tile_rect):
                # Check if the enemy is standing on a block from above
                if enemy_rect.bottom > tile_rect.top and self.enemy.pos_y < tile_rect.top:
                    self.enemy.pos_y = tile_rect.top - self.enemy.height
                # Check if the enemy bumps into a block from below
                # checked that the bottom edge of the enemy is below the bottom edge of the block
                elif enemy_rect.top < tile_rect.bottom and self.enemy.pos_y + self.enemy.height > tile_rect.bottom:
                    self.enemy.pos_y = tile_rect.bottom
                # Checking if the enemy bumps into a block from the right
                elif enemy_rect.right > tile_rect.left and self.enemy.pos_x < tile_rect.left:
                    self.enemy.pos_x = tile_rect.left - self.enemy.width
                # Check if the enemy bumps into a block from the left
                elif enemy_rect.left < tile_rect.right and self.enemy.pos_x + self.enemy.width > tile_rect.right:
                    self.enemy.pos_x = tile_rect.right

        # enemy collision list
        for self.enemy in self.enemy_list:  
            # enemy collision for list enemies
            enemy_rect = pygame.Rect(self.enemy.pos_x, self.enemy.pos_y, self.enemy.width, self.enemy.height)
            # check if the rectangle of the enemy overlaps with the rectangle of the block
            for tile in self.tile_list:
                tile_rect = tile[1]
                if enemy_rect.colliderect(tile_rect):
                    # Check if the enemy is standing on a block from above
                    if enemy_rect.bottom > tile_rect.top and self.enemy.pos_y < tile_rect.top:
                        self.enemy.pos_y = tile_rect.top - self.enemy.height
                    # Check if the enemy bumps into a block from below
                    # checked that the bottom edge of the enemy is below the bottom edge of the block
                    elif enemy_rect.top < tile_rect.bottom and self.enemy.pos_y + self.enemy.height > tile_rect.bottom:
                        self.enemy.pos_y = tile_rect.bottom
                    # Checking if the enemy bumps into a block from the right
                    elif enemy_rect.right > tile_rect.left and self.enemy.pos_x < tile_rect.left:
                        self.enemy.pos_x = tile_rect.left - self.enemy.width
                    # Check if the enemy bumps into a block from the left
                    elif enemy_rect.left < tile_rect.right and self.enemy.pos_x + self.enemy.width > tile_rect.right:
                        self.enemy.pos_x = tile_rect.right
            
            if self.player.pos_x < self.enemy.pos_x + self.enemy.width and self.player.pos_x + self.player.width > self.enemy.pos_x:
                if self.player.pos_y < self.enemy.pos_y + self.enemy.height and self.player.pos_y + self.player.height > self.enemy.pos_y:
                    return True

        return False
    
    # reset the game if the player was catched by the enemy
    def reset_game(self):
        self.player.pos_x = self.tile_size*3
        self.player.pos_y = self.tile_size*18.5
        self.enemy.pos_x = random.randint(0, self.display_width - 40)
        self.enemy.pos_y = random.randint(0, self.display_height - 40)

        self.enemy_list = [self.enemy]
        self.sound_game_over_check= False
        self.sound_played = False
        self.sound_menu_check = False
        self.game_over_sound.stop()
        self.game_sound.stop()
        self.sound(sound_game_over_check=self.sound_game_over_check,sound_menu_check=self.sound_menu_check,sound_played=self.sound_played)
        # for scoring
        self.game_score = 0
        

    def create_world(self):
        # placed den screen (Start at x = 0 and y =0)
        self.screen.blit(self.background, (0, 0))
        # placed the player into the window
        self.player.draw(self.screen)
        # placed the enemy into the window
        #self.enemy.draw(self.screen)
        #self.draw_grid()
        self.draw()
        for self.a in self.enemy_list:
            self.a.draw(self.screen)
            self.a.move_towards_player(self.player)
        # set game status = true
        self.game_started = True
        pygame.display.update()
    
    # music controlling
    def sound(self, sound_played, sound_menu_check, sound_game_over_check):   

            # games sound config
            # menu sound
            if not self.game_started:
                if not self.sound_menu_check:
                    self.menu_sound.play(-1)
                    self.sound_menu_check = True
                    return sound_menu_check
            # game sound sound
            if self.game_started:
                self.menu_sound.stop()
                if not self.sound_played:
                    self.game_sound.play(-1)
                    self.sound_played = True
                    return self.sound_played

    # function to end the game 
    def exit_game_function(self):
        pygame.quit()
        sys.exit()

    # function to handle mute button
    def sound_mute(self):
        self.mute_sound = True

    # function to handle no mute button
    def sound_no_mute(self):
        self.mute_sound = False

    # primary run function
    def run(self):
        self.game_score=int(0)
        #start from pygame
        pygame.init()
        # create a screen with the dimensions
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        # set the game name
        pygame.display.set_caption("Sand")
        # objects for buttons
        draw_mute_button= Button(x=(self.display_width // 2 +355),y=(self.display_height // 2 - 400), width=200, height=100, callback=self.sound_mute)
        draw_no_mute_button= Button(x=(self.display_width // 2 +306),y=(self.display_height // 2 - 400), width=60, height=100, callback=self.sound_no_mute)
        start_button = Button(x=(self.display_width // 2 - 100),y=(self.display_height // 2 - 50), width=200, height=100, callback=self.create_world)
        exit_button = Button(x=(self.display_width // 2 - 100),y=(self.display_height // 2 - -80), width=200, height=100, callback=self.exit_game_function)
        headline = Button(x=(self.display_width // 8),y=(self.display_height // 8 * 1.1), width=200, height=100, callback=None)
        score = Button(x=(self.display_width // 4),y=(self.display_height // 2 - -250), width=200, height=100, callback=None)
        # get and format best scores
        self.highscore_font_size = 48
        # format text
        self.score_text = self.game_over_font_text.render("Highscore:", True, (0, 0, 0))
        best_score = self.game_over_font_text_score.render(f"{self.scoringHandler.get_score()}", True, (0, 0, 0))
        # event for new enemy
        new_enemy = pygame.USEREVENT
        
        pygame.time.set_timer(new_enemy, 10000)

        # Sound-Flag hinzufügen
        self.sound_played = False
        self.sound_menu_check = False
        self.sound_game_over_check = False

        # main loop
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # check game started event
                if not self.game_started:
                    start_button.handle_event(event)

                # check game started event
                if not self.game_started:
                    draw_mute_button.handle_event(event)

                # check game started event
                if not self.game_started:
                    draw_no_mute_button.handle_event(event)
                    
                # check game exit event
                if not self.game_exit:
                    exit_button.handle_event(event)

                # check game enemy event
                if event.type == new_enemy and self.game_started:
                    # create new enemies and append them to the list
                    test = Enemy(random.randint((self.player.pos_x + 80), self.display_width - 40), random.randint(self.player.pos_x + 80, self.display_height - 40),
                                 width=40, height=40, speed=2)
                    self.enemy_list.append(test)
            
                # game_score
                if self.game_started: 
                    self.game_score += 1

            keys = pygame.key.get_pressed()

            # music
            if self.mute_sound != True: 
                self.menu_sound.set_volume(10)
                self.game_sound.set_volume(10)
                self.game_over_sound.set_volume(10)
                self.sound(sound_game_over_check=self.sound_game_over_check, sound_menu_check=self.sound_menu_check, sound_played = self.sound_played )
            else:
                self.menu_sound.set_volume(0)
                self.game_sound.set_volume(0)
                self.game_over_sound.set_volume(0)

            # if var = true // player active
            if self.game_started:
                self.player.move(keys, self.display_width, self.display_height)

            # handle the gameover properties (collision between player, enemies and objects)
            if self.game_started:
                if self.check_collision():
                    # game over sound
                    # change game sound to game over sound
                    if self.mute_sound != True: 
                        self.game_sound.stop()
                        self.game_over_sound.play(-1)
                        self.sound_game_over_check = True
                    self.scoringHandler.save_score(game_score=self.game_score)
                    self.show_game_over()
                    self.reset_game()

            # set the background images as background for the screen
            self.screen.blit(self.background, (0, 0))
            
            # if button is not triggered draw the start button at the screen
            if not self.game_started:
                start_button.draw_start_button(self.screen)
                exit_button.draw_exit_button(self.screen)
                headline.draw_headline(self.screen)
                score.draw_score(self.screen)
                draw_mute_button.draw_mute_button(self.screen)
                draw_no_mute_button.draw_no_mute_button(self.screen)
                # rendering the event text
                # game_over_score_text
                self.screen.blit(self.score_text, (self.display_width // 2 - self.score_text.get_width() // 2, self.display_height // 2 - self.score_text.get_height() // 2 - -310))
                self.screen.blit(best_score, (self.display_width // 2 - best_score.get_width() // 2, self.display_height // 2 - best_score.get_height() // 2 - -350))
                
            # if button (start) triggered create the world
            if self.game_started:
                self.create_world()      

             # if button (exit) triggered exit the game
            if self.game_exit:
                self.exit_game_function() 

            #Update the display in the loop
            pygame.display.flip()
            # set 30 images per second 
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
