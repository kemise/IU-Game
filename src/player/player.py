import pygame


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