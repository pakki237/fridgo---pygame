import pygame
from settings import*
from physics import*
from obstacle import*
pygame.init()
print(pygame.version.ver)
clock = pygame.time.Clock()

from player import Player





screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
player = Player()
pygame.display.set_caption("FRIDGO")

running = True

while running:
    dt = clock.tick(FPS) / 1000
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.direction = -1
    if keys[pygame.K_d]:
        player.direction = 1
    if keys[pygame.K_w]:
        player.direction = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and player.on_ground:  #key pressed
            if event.key == pygame.K_SPACE:
                player.charging = True
               
        if event.type == pygame.KEYUP:   #key released
            if event.key == pygame.K_SPACE:
                player.charging = False
                
                player.velocity_y = -(player.charge*30)
                player.velocity_x = player.direction*player.charge*20
                    
                player.on_ground = False
                player.charge = 0
    if player.charging:
        player.charge += 25*dt

        if player.charge > MAX_CHARGE:
            player.charge = MAX_CHARGE
   
    # if keys[pygame.K_a]:
    #     frog_x -=2
    # if keys[pygame.K_d]:
    #         frog_x +=2
    if player.x < 0:
         player.x = 0
    if player.x + player.width > WIDTH:
        player.x = WIDTH - player.width

    previous_x = player.x
    previous_y = player.y
    #physics
   
    update_physics(player,dt,platforms)

    
        
    pygame.display.set_caption(f"FRIDGO | FPS: {clock.get_fps():.1f}")
    screen.fill((135,206,235))
    pygame.draw.rect(screen,  (139, 69, 19), (0,HEIGHT - GROUND_HEIGHT,WIDTH, GROUND_HEIGHT)) #x,y,width,height
    for platform in platforms:
        pygame.draw.rect(screen,(100,100,100),platform)
    screen.blit(player.image, (int(player.x), int(player.y)))
    pygame.display.flip()

    
   


pygame.quit()

