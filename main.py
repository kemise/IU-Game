
import pygame
import sys
import random

pygame.init()

class Player:
    def __init__(self, pos_x, pos_y, width, height, speed):
        #position
        self.pos_x = pos_x
        self.pos_y = pos_y
        #dimension
        self.width = width
        self.height = height
        #speed
        self.speed = speed
        # list with images for the walk animation
        self.animation_frames = [pygame.image.load(f"./assets/images/player/hero/hero_walk_{i}.png") for i in range(1, 5)]
        # current image
        self.current_frame = 0
        # test criterion whether the figure is moving
        self.is_walking = False
        

    def move(self, keys, display_width, display_height):
        self.is_walking = False
        if keys[pygame.K_UP] and self.pos_y > 0:
            self.pos_y -= self.speed
        elif keys[pygame.K_RIGHT] and self.pos_x + self.width < display_width:
            self.pos_x += self.speed
            #set to true and thus enable the index to be censored
            self.is_walking = True
        elif keys[pygame.K_DOWN] and self.pos_y + self.height < display_height:
            self.pos_y += self.speed
        elif keys[pygame.K_LEFT] and self.pos_x > 0:
            self.pos_x -= self.speed
            #set to true and thus enable the index to be censored
            self.is_walking = True


        # Index, which is counted on the basis of movement.
        # Not longer than the image list and is reset with modulo.
        # Index is then used for the selection of the image to be run
        if self.is_walking:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw(self, screen):
        # Select and display the current picture from the list, only when the right and left buttons are pressed.d
        if self.is_walking:
            current_image = self.animation_frames[self.current_frame]

            
        else:
            # Show the first image when not running
            current_image = self.animation_frames[0]  
        # scaled the asset
        scaled_player_image = pygame.transform.scale(current_image, (self.width, self.height))
        # draw it in the window
        screen.blit(scaled_player_image, (self.pos_x, self.pos_y))
                        


class Enemy:
    def __init__(self, pos_x, pos_y, width, height, speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        # list with images for the walk animation
        self.animation_frames = [pygame.image.load(f"./assets/images/player/enemy/enemy_walk_{i}.png") for i in range(1, 6)]
        # current image
        self.current_frame = 0
        # test criterion whether the figure is moving
        self.is_walking = False 



    # control the movement of the opponent
    def move_towards_player(self, player):
        target_x = player.pos_x
        target_y = player.pos_y

        # Check whether speed is greater than the distance and then use the smaller value with min. This prevents inconsistency/flickering.
        if self.pos_x < target_x:
            self.pos_x += min(self.speed, target_x - self.pos_x)
            #set to true and thus enable the index to be censored
            self.is_walking = True
        elif self.pos_x > target_x:
            self.pos_x -= min(self.speed, self.pos_x - target_x)
            #set to true and thus enable the index to be censored
            self.is_walking = True
        elif self.pos_y < target_y:
            self.pos_y += min(self.speed, target_y - self.pos_y)
            #set to true and thus enable the index to be censored
            self.is_walking = True
        elif self.pos_y > target_y:
            self.pos_y -= min(self.speed, self.pos_y - target_y)
            #set to true and thus enable the index to be censored
            self.is_walking = True

        if self.is_walking:
            
                    self.current_frame = (self.current_frame + 1) % len(self.animation_frames)


    # draw the enemy
    def draw(self, screen):
        # Select and display the current picture from the list, only when the right and left buttons are pressed.d
        if self.is_walking:
            current_image = self.animation_frames[self.current_frame]  
        else:
            # Show the first image when not running
            current_image = self.animation_frames[0]  
        # scaled the asset
        scaled_enemy_image = pygame.transform.scale(current_image, (self.width, self.height))
        # draw it in the window
        screen.blit(scaled_enemy_image, (self.pos_x, self.pos_y))    




        




class Game:
    def __init__(self):
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
        self.player = Player(pos_x=self.tile_size*3, pos_y=self.tile_size*18.5, width=30, height=30, speed=5)
        # enemy setting
        self.enemy = Enemy(random.randint(0, self.display_width-40), random.randint(0, self.display_height-40), width=40, height=40, speed=3)
        # for game over event
        self.game_over_font = pygame.font.SysFont(None, 80)
        # screen name
        pygame.display.set_caption("MyGame")
        self.go = True
        # asset images
        grass_img = pygame.image.load("./assets/images/StoneBlock.png")
        dirt_img = pygame.image.load("./assets/images/Stone.png")    
        # placeholder for assets (map)
        self.tile_list = []
        row_count = 0
        # map structure
        self.world_data = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2], 
            [2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 2], 
            [2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2], 
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2], 
            [2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2], 
            [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2], 
            [2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2], 
            [2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2], 
            [2, 0, 2, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2], 
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
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
    def draw_grid(self):
        for line in range(0, 20):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * self.tile_size), (self.display_width, line * self.tile_size))
            pygame.draw.line(self.screen, (255, 255, 255), (line * self.tile_size, 0), (line * self.tile_size, self.display_height))

    # display tile on screen
    def draw(self):
        # display each tile from the list on the screen
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])


    def show_game_over(self):
        # event text
        game_over_text = self.game_over_font.render("Game Over", True, (255, 0, 0))
        restart_text = self.game_over_font.render("Press 'R' to play again", True, (255, 0, 0))
        close_text = self.game_over_font.render("Press 'C' to close", True, (255, 0, 0))
        # rendering the event text
        self.screen.blit(game_over_text, (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 2 - game_over_text.get_height() // 2))
        self.screen.blit(restart_text, (self.display_width // 2 - restart_text.get_width() // 2, self.display_height // 2 + game_over_text.get_height() // 2 + 60))
        self.screen.blit(close_text, (self.display_width // 2 - close_text.get_width() // 2, self.display_height // 2 + game_over_text.get_height() // 2 + 130))
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
        self.enemy_list = []
        self.enemy_list = [self.enemy]


    def create_world(self):
        # placed den screen (Start at x = 0 and y =0)
        self.screen.blit(self.background, (0, 0))
        # placed the player into the window
        self.player.draw(self.screen)
        # placed the enemy into the window
        #self.enemy.draw(self.screen)
        self.draw_grid()
        self.draw()
        for self.a in self.enemy_list:
            self.a.draw(self.screen)
            self.a.move_towards_player(self.player)
        # set game status = true
        self.game_started = True
        pygame.display.update()
    

    # function to end the game 
    def exit_game_function(self):
        pygame.quit()
        sys.exit()

    
    
    # primary run function
    def run(self):
        #start from pygame
        pygame.init()
        # create a screen with the dimensions
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        # set the game name
        pygame.display.set_caption("Spielname")
        # objects for buttons
        start_button = Button(x=(self.display_width // 2 - 100),y=(self.display_height // 2 - 50), width=200, height=100, callback=self.create_world)
        exit_button = Button(x=(self.display_width // 2 - 100),y=(self.display_height // 2 - -80), width=200, height=100, callback=self.exit_game_function)
        headline = Button(x=(self.display_width // 8),y=(self.display_height // 8 * 1.1), width=200, height=100, callback=None)

        new_enemy = pygame.USEREVENT
        
        pygame.time.set_timer(new_enemy, 10000)


        # main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # check game started event
                if not self.game_started:
                    start_button.handle_event(event)
                    
                # check game exit event
                if not self.game_exit:
                    exit_button.handle_event(event)

                # check game enemy event
                if event.type == new_enemy:
                    # create new enemies and append them to the list
                    test = Enemy(random.randint(0, self.display_width - 40), random.randint(0, self.display_height - 40),
                                 width=40, height=40, speed=2)
                    self.enemy_list.append(test)

            keys = pygame.key.get_pressed()

            # if var = true // player active
            if self.game_started:
                self.player.move(keys, self.display_width, self.display_height)

            # handle the collision between player, enemies and objects
            if self.check_collision():
                self.show_game_over()
                self.reset_game()

            # set the background images as background for the screen
            self.screen.blit(self.background, (0, 0))
            
            # if button is not triggered draw the start button at the screen
            if not self.game_started:
                start_button.draw_start_button(self.screen)
                exit_button.draw_exit_button(self.screen)
                headline.draw_headline(self.screen)
                
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


class Button:
    def __init__(self, x, y, width, height, callback):

        self.rect = pygame.Rect(x, y, width, height)
        # images for the buttons
        self.start_image = pygame.image.load("./assets/images/Buttons/start_button.png")
        self.exit_image = pygame.image.load("./assets/images/Buttons/exit_button.png")
        self.headline_image = pygame.image.load("./assets/images/Buttons/headline.png")
        #  button image scaling
        self.start_button = pygame.transform.scale(self.start_image, (200, 100))  
        self.exit_button = pygame.transform.scale(self.exit_image, (200, 100))  
        self.headline = pygame.transform.scale(self.headline_image, (600, 150))  
        # action for the button
        self.callback = callback
    
    # draw the button
    def draw_start_button(self, surface):
        surface.blit(self.start_button, self.rect.topleft)

    def draw_exit_button(self, surface):
        surface.blit(self.exit_button, self.rect.topleft)

    def draw_headline(self, surface):
        surface.blit(self.headline, self.rect.topleft)
    
    # event handler
    # mouse click
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
    






if __name__ == "__main__":
    game = Game()
    game.run()