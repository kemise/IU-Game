import pygame

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pygame.init

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

    def find_shortest_path(self, player):
        TILE_SIZE = 40

        # Berechne die Zielkachel, auf der der Spieler sich befindet
        target_tile_x = int(player.pos_x // TILE_SIZE)

        target_tile_y = int(player.pos_y // TILE_SIZE)

        # Erstelle die Spielfeldmatrix game_matrix
        game_matrix = [
            [0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0],
            [0	,1	,1	,1	,1	,1	,1	,1	,1	,1	,0	,1	,1	,0	,1	,1	,1	,1	,1	,0],
            [0	,1	,1	,1	,0	,0	,0	,0	,0	,1	,0	,1	,1	,0	,1	,1	,1	,1	,1	,0],
            [0	,0	,1	,1	,1	,1	,1	,0	,0	,1	,0	,1	,1	,0	,1	,1	,0	,1	,1	,0],
            [0	,1	,1	,1	,1	,1	,1	,0	,0	,1	,0	,1	,1	,0	,1	,1	,0	,1	,1	,0],
            [0	,1	,1	,1	,1	,1	,1	,0	,0	,1	,1	,1	,1	,1	,1	,1	,0	,1	,0	,0],
            [0	,0	,0	,0	,1	,1	,1	,1	,0	,1	,1	,1	,1	,1	,1	,1	,0	,1	,1	,0],
            [0	,1	,0	,1	,1	,1	,1	,1	,0	,0	,0	,1	,0	,0	,0	,1	,0	,1	,1	,0],
            [0	,1	,0	,1	,1	,1	,1	,1	,0	,1	,1	,1	,1	,0	,1	,1	,0	,1	,1	,0],
            [0	,1	,0	,1	,1	,1	,1	,0	,0	,1	,1	,1	,1	,0	,1	,1	,0	,1	,0	,0],
            [0	,1	,1	,1	,0	,1	,1	,1	,0	,1	,1	,1	,1	,0	,1	,1	,0	,1	,1	,0],
            [0	,1	,1	,1	,0	,1	,1	,1	,0	,1	,0	,1	,1	,1	,1	,1	,0	,1	,1	,0],
            [0	,1	,1	,1	,0	,1	,1	,1	,0	,1	,0	,1	,1	,1	,1	,1	,0	,1	,1	,0],
            [0	,1	,1	,1	,0	,0	,1	,1	,1	,1	,0	,0	,0	,0	,0	,1	,0	,0	,1	,0],
            [0	,1	,0	,0	,0	,1	,1	,0	,1	,1	,0	,1	,1	,1	,1	,1	,1	,0	,1	,0],
            [0	,1	,0	,1	,0	,1	,1	,0	,1	,1	,0	,1	,1	,1	,1	,1	,1	,1	,1	,0],
            [0	,1	,0	,1	,0	,1	,1	,0	,0	,0	,0	,1	,0	,0	,0	,1	,1	,1	,1	,0],
            [0	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,1	,0	,1	,0],
            [0	,1	,1	,1	,0	,1	,1	,0	,1	,1	,1	,1	,1	,1	,1	,1	,1	,0	,1	,0],
            [0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0	,0]
            ]

        # Erstelle die game_grid Grid-Instanz
        game_grid = Grid(matrix=game_matrix)

        # Startknoten (gegnerische Position)
        start_x = (self.pos_x // TILE_SIZE)
        start_y =(self.pos_y // TILE_SIZE)


        start_node = game_grid.node(start_x,start_y)


        # Zielknoten (Spielerposition)

        target_node = game_grid.node(target_tile_x, target_tile_y)

        # Verwende den A*-Algorithmus, um den kürzesten Weg zu finden
        finder = AStarFinder()
        path, runs = finder.find_path(start=start_node, end=target_node, grid=game_grid)
        return path

    # control the movement of the opponent
    def move_towards_player(self, player):
        TILE_SIZE = 40

        # Umwandlung der Pixelkoordinaten in Rasterkoordinaten
        target_tile_x = int(player.pos_x // TILE_SIZE)
        target_tile_y = int(player.pos_y // TILE_SIZE)

        # Finde den kürzesten Weg zum Spieler
        shortest_path = self.find_shortest_path(player)

        if len(shortest_path) > 1:
            # Nächsten Schritt aus dem kürzesten Weg auswählen
            next_tile_x, next_tile_y = shortest_path[1]

            # Zielposition in Pixeln berechnen
            target_x = next_tile_x * TILE_SIZE
            target_y = next_tile_y * TILE_SIZE

            # Bestimme die Richtung, in die sich der Gegner bewegen soll
            move_x = 0
            move_y = 0

            if self.pos_x < target_x:
                move_x = 1
            elif self.pos_x > target_x:
                move_x = -1

            if self.pos_y < target_y:
                move_y = 1
            elif self.pos_y > target_y:
                move_y = -1

            # Bewege den Gegner in der entsprechenden Richtung
            self.pos_x += move_x * self.speed
            self.pos_y += move_y * self.speed

            self.is_walking = True

            # Inkrementiere den Animationsframe, wenn sich der Gegner bewegt
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
