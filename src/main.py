import pygame
from settings import*
from player import*
from physics import*
from obstacle import*
pygame.init()
clock = pygame.time.Clock()






screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FRIDGO")

running = True

while running:
    dt = clock.tick(120) / 1000
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        direction = -1
    if keys[pygame.K_d]:
        direction = 1
    if keys[pygame.K_w]:
        direction = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and on_ground:  #key pressed
            if event.key == pygame.K_SPACE:
                charging = True
               
        if event.type == pygame.KEYUP:   #key released
            if event.key == pygame.K_SPACE:
                charging = False
                
                velocity_y = -(charge*30)
                velocity_x = direction*charge*20
                    
                on_ground = False
                charge = 0
    if charging:
        charge += 25*dt

        if charge > max_charge:
            charge = max_charge
   
    # if keys[pygame.K_a]:
    #     frog_x -=2
    # if keys[pygame.K_d]:
    #         frog_x +=2
    if frog_x < 0:
         frog_x = 0
    if frog_x + frog_width > WIDTH:
        frog_x = WIDTH - frog_width

    #physics
    Frog_rect = pygame.Rect(frog_x,frog_y,frog_width,frog_height)
    Platform_rect = pygame.Rect(platform_x,platform_y,platform_width,platform_height)
    frog_x,frog_y,velocity_x, velocity_y, on_ground = update_physics(
    frog_x,
    frog_y,
    velocity_x,
    velocity_y,
    on_ground,
    dt
    )
    if Frog_rect.colliderect(Platform_rect):
        print("collision")
    

    screen.fill((135,206,235))
    pygame.draw.rect(screen,  (139, 69, 19), (0,HEIGHT - GROUND_HEIGHT,WIDTH, GROUND_HEIGHT)) #x,y,width,height
    pygame.draw.rect(screen,(100,100,100),(platform_x,platform_y,platform_width,platform_height))
    pygame.draw.rect(screen, (0, 255, 0), (frog_x, frog_y, frog_width, frog_height)) #all the variables has been changed by proper variables
    pygame.display.update()
   


pygame.quit()

