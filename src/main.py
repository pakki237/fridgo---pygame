import pygame
pygame.init()
clock = pygame.time.Clock()

WIDTH = 900
HEIGHT = 600
GROUND_HEIGHT = 50

charging = False
charge = 0
max_charge = 30
jump_multiplier = 0.20
MAX_FALL_SPEED = 900


frog_width =50
frog_height = 50
frog_x = 100
frog_y =  HEIGHT - GROUND_HEIGHT - frog_height


velocity_y =0
on_ground = True
gravity = 1800   # pixels per second²

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FRIDGO")

running = True

while running:
    dt = clock.tick(120) / 1000
    keys = pygame.key.get_pressed()
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
                    
                on_ground = False
                charge = 0
    if charging:
        charge += 20*dt

        if charge > max_charge:
            charge = max_charge
    print(charge)
    # if keys[pygame.K_a]:
    #     frog_x -=2
    # if keys[pygame.K_d]:
    #         frog_x +=2
    if frog_x < 0:
         frog_x = 0
    if frog_x + frog_width > WIDTH:
         frog_x = WIDTH - frog_width
    

    if not on_ground:
        velocity_y += gravity * dt

    if velocity_y > MAX_FALL_SPEED:

         velocity_y = MAX_FALL_SPEED

    frog_y +=velocity_y*dt

    ground_y = HEIGHT - GROUND_HEIGHT
    if frog_y + frog_height >= ground_y:
        frog_y = ground_y - frog_height
        velocity_y = 0
        on_ground =True
   

    screen.fill((135,206,235))
    pygame.draw.rect(screen,  (139, 69, 19), (0,HEIGHT - GROUND_HEIGHT,WIDTH, GROUND_HEIGHT)) #x,y,width,height
    pygame.draw.rect(screen, (0, 255, 0), (frog_x, frog_y, frog_width, frog_height)) #all the variables has been changed by proper variables
    pygame.display.update()
   


pygame.quit()

