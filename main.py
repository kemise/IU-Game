import pygame
import sys
import random

pygame.init()

class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        

    def move(self, keys, display_width, display_height):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.width < display_width:
            self.x += self.speed
        if keys[pygame.K_DOWN] and self.y + self.height < display_height:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

    def draw(self, screen):
        # loade asset
        player_char = pygame.image.load("./assets/images/player/hero/hero_walk_1.png")
        # scaled the asset
        scaled_player_image = pygame.transform.scale(player_char, (self.width, self.height))
        # show enemy on screen
        screen.blit(scaled_player_image, (self.x, self.y))        

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_towards_player(self, player):
        target_x = player.x
        target_y = player.y

        if self.x < target_x:
            self.x += min(self.speed, target_x - self.x)
        elif self.x > target_x:
            self.x -= min(self.speed, self.x - target_x)

        if self.y < target_y:
            self.y += min(self.speed, target_y - self.y)
        elif self.y > target_y:
            self.y -= min(self.speed, self.y - target_y)

    def draw(self, screen):
        # loade asset
        enemy_char = pygame.image.load("./assets/images/player/enemy/enemy_walk_1.png")
        # scaled the asset
        scaled_enemy_image = pygame.transform.scale(enemy_char, (self.width, self.height))
        # show enemy on screen
        screen.blit(scaled_enemy_image, (self.x, self.y))




class Game:
    def __init__(self):
        self.display_width = 800
        self.display_height = 800
        self.screen = pygame.display.set_mode([self.display_width, self.display_height])
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("./assets/images/world/BG.png")
        self.player = Player(x=100, y=100, width=30, height=30, speed=7)
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
        if self.player.x < self.enemy.x + self.enemy.width and self.player.x + self.player.width > self.enemy.x:
            if self.player.y < self.enemy.y + self.enemy.height and self.player.y + self.player.height > self.enemy.y:
                return True
        return False
    
    # reset the game if the player was catched by the enemy
    def reset_game(self):
        self.player.x = 100
        self.player.y = 100
        self.enemy.x = random.randint(0, self.display_width - 40)
        self.enemy.y = random.randint(0, self.display_height - 40)

    def create_world(self):
        # platziere den screen (Start bei x = 0 und y = 0)
        self.screen.blit(self.background, (0, 0))
        # platziere den spieler im screen
        self.player.draw(self.screen)
        # platziere den gegner im spiel
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
