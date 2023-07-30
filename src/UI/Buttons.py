
import pygame

pygame.init()


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
    

