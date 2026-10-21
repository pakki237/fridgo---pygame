from settings import*
import pygame


gravity = 1800   # pixels per second²

AIR_FRICTION = 1.0
GROUND_FRICTION = 10.0

def update_physics(player,dt,platforms):

    player.previous_x =player.x
    player.previous_y =player.y
    
    if not player.on_ground:
            if player.velocity_y < 0:
                  player.velocity_y +=GRAVITY_UP*dt
            else:
                  player.velocity_y +=GRAVITY_DOWN*dt
             
    
    if player.velocity_y > MAX_FALL_SPEED:
      
             player.velocity_y = MAX_FALL_SPEED

   
    if not player.on_ground:
        player.velocity_x -= player.velocity_x*AIR_FRICTION*dt
    else:
        player.velocity_x -= player.velocity_x*GROUND_FRICTION*dt  

    player.y +=player.velocity_y*dt
    player.x +=player.velocity_x*dt
    ground_y = HEIGHT - GROUND_HEIGHT
    if player.y + player.height >= ground_y:
            player.y = ground_y - player.height
            player.velocity_y = 0
            player.on_ground =True
    Frog_rect = pygame.Rect(player.x,player.y,player.width,player.height)
    for platform in platforms:
          
        if Frog_rect.colliderect(platform):
            if player.previous_y + player.height <= platform.top:
                player.y = platform.top - player.height
                player.velocity_y = 0
                player.on_ground = True
    