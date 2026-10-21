import pygame

platform_x = 300
platform_y = 400

platform_width =200
platform_height =30

platform_rect = pygame.Rect(

    platform_x,

    platform_y,

    platform_width,

    platform_height

)
platforms = [
    pygame.Rect(300, 400, 200, 30),

    pygame.Rect(550, 300, 180, 30),

    pygame.Rect(750, 200, 150, 30),

    pygame.Rect(100, 250, 150, 30),
]