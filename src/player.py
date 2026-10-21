import pygame
from settings import*

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - GROUND_HEIGHT - FROG_HEIGHT

        self.previous_x = self.x
        self.previous_y = self.y

        self.width = FROG_WIDTH
        self.height = FROG_HEIGHT
               
        self.image = pygame.image.load("assets/fridgo1.png").convert_alpha()
        self.image = self.image.subsurface(self.image.get_bounding_rect()).copy()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = True

        self.charge = 0

        self.charging = False

        self.direction = 1
