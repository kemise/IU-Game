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
        if keys[pygame.K_RIGHT] and self.pos_x + self.width < display_width:
            self.pos_x += self.speed
            #set to true and thus enable the index to be censored
            self.is_walking = True
        if keys[pygame.K_DOWN] and self.pos_y + self.height < display_height:
            self.pos_y += self.speed
        if keys[pygame.K_LEFT] and self.pos_x > 0:
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
        # zeichne es im window
        screen.blit(scaled_player_image, (self.pos_x, self.pos_y))
                        


class Enemy:
    def __init__(self, pos_x, pos_y, width, height, speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed

    # control the movement of the opponent
    def move_towards_player(self, player):
        target_x = player.pos_x
        target_y = player.pos_y

        # Check whether speed is greater than the distance and then use the smaller value with min. This prevents inconsistency/flickering.
        if self.pos_x < target_x:
            self.pos_x += min(self.speed, target_x - self.pos_x)
        elif self.pos_x > target_x:
            self.pos_x -= min(self.speed, self.pos_x - target_x)

        if self.pos_y < target_y:
            self.pos_y += min(self.speed, target_y - self.pos_y)
        elif self.pos_y > target_y:
            self.pos_y -= min(self.speed, self.pos_y - target_y)

    def draw(self, screen):
        # loade asset
        enemy_char = pygame.image.load("./assets/images/player/enemy/enemy_walk_1.png")
        # scaled the asset
        scaled_enemy_image = pygame.transform.scale(enemy_char, (self.width, self.height))
        # show enemy on screen
        screen.blit(scaled_enemy_image, (self.pos_x, self.pos_y))




class Game:
    def __init__(self):
        self.display_width = 1200
        self.display_height = 800
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("./assets/images/world/BG.png")
        self.player = Player(pos_x=100, pos_y=100, width=30, height=20, speed=7)
        self.enemy = Enemy(random.randint(0, self.display_width-40), random.randint(0, self.display_height-40), width=50, height=50, speed=5)
        self.game_over_font = pygame.font.SysFont(None, 80)
        pygame.display.set_caption("MyGame")
        self.go = True


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

                

    # check the collision
    def check_collision(self):
        if self.player.pos_x < self.enemy.pos_x + self.enemy.width and self.player.pos_x + self.player.width > self.enemy.pos_x:
            if self.player.pos_y < self.enemy.pos_y + self.enemy.height and self.player.pos_y + self.player.height > self.enemy.pos_y:
                return True
        return False
    
    # reset the game if the player was catched by the enemy
    def reset_game(self):
        self.player.pos_x = 100
        self.player.pos_y = 100
        self.enemy.pos_x = random.randint(0, self.display_width - 40)
        self.enemy.pos_y = random.randint(0, self.display_height - 40)

    def create_world(self):
        # placed den screen (Start bei x = 0 und y = 0)
        self.screen.blit(self.background, (0, 0))
        # placed the player into the window
        self.player.draw(self.screen)
        # placed the enemy into the window
        self.enemy.draw(self.screen)
        pygame.display.update()


        

    def run(self):
            
            while self.go:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        go = False

                keys = pygame.key.get_pressed()
                self.player.move(keys, self.display_width, self.display_height)
                self.enemy.move_towards_player(self.player)

                if self.check_collision():
                    self.show_game_over()
                    self.reset_game()

                self.create_world()
                self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
