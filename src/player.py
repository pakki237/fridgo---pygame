import os
import pygame
from settings import *


class Player:
    def __init__(self):
        self.sprite_y_offset = 12
        self.x = 100
        self.y = HEIGHT - GROUND_HEIGHT - FROG_HEIGHT

        self.previous_x = self.x
        self.previous_y = self.y

        self.width = FROG_WIDTH
        self.height = FROG_HEIGHT

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = True
        self.charge = 0
        self.charging = False

        # 1 = right, -1 = left
        self.direction = 0

        # Path to the assets folder
        asset_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets"
        )

        # Load the four frog sprites
        self.image_front = pygame.image.load(

             os.path.join(asset_path, "fridgo1.png")
        )
        self.image_front_up = pygame.image.load(
        
            os.path.join(asset_path, "fridgo-up.png")
        )
        self.image_right = pygame.image.load(
            os.path.join(asset_path, "fridgo-right1.png")
        )

        self.image_left = pygame.image.load(
            os.path.join(asset_path, "fridgo-left.png")
        )

        self.image_jump_right = pygame.image.load(
            os.path.join(asset_path, "fridgo-rightjump.png")
        )

        self.image_jump_left = pygame.image.load(
            os.path.join(asset_path, "fridgo-leftjump.png")
        )

        
        sprite_size = (self.width, self.height)
        # Scale images to the player's dimensions
        # Make the front-facing frog slightly larger

        front_size = (int(self.width * 1.05), int(self.height * 1.05))
        self.image_front = pygame.transform.scale(
            self.image_front, front_size
        )  
        self.image_front_up =pygame.transform.scale(
            self.image_front_up, front_size
        )  
        self.image_right = pygame.transform.scale(
            self.image_right, sprite_size
        )

        self.image_left = pygame.transform.scale(
            self.image_left, sprite_size
        )

        self.image_jump_right = pygame.transform.scale(
            self.image_jump_right, sprite_size
        )

        self.image_jump_left = pygame.transform.scale(
            self.image_jump_left, sprite_size
        )
    def get_image(self):
        # Jumping sprites
        if not self.on_ground:
            if self.direction == 0:
                return self.image_front_up
            elif self.direction == -1:
                return self.image_jump_left
            else:
                return self.image_jump_right

        # Standing sprites
        if self.direction == 0:
            return self.image_front
        elif self.direction == -1:
            return self.image_left
        else:
            return self.image_right