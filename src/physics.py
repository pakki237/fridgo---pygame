from settings import*
from player import*

velocity_y =0
velocity_x =0 #horizontal velocity
direction = 1


on_ground = True
gravity = 1800   # pixels per second²

AIR_FRICTION = 1.0
GROUND_FRICTION = 10.0

def update_physics(frog_x,frog_y,velocity_x,velocity_y,on_ground,dt):
   
    
    if not on_ground:
            velocity_y += gravity * dt
    
    if velocity_y > MAX_FALL_SPEED:
      
             velocity_y = MAX_FALL_SPEED
    
    frog_y +=velocity_y*dt
    frog_x +=velocity_x*dt
    if not on_ground:
        velocity_x -= velocity_x*AIR_FRICTION*dt
    else:
        velocity_x -= velocity_x*GROUND_FRICTION*dt  
    ground_y = HEIGHT - GROUND_HEIGHT
    if frog_y + frog_height >= ground_y:
            frog_y = ground_y - frog_height
            velocity_y = 0
            on_ground =True
    return frog_x,frog_y,velocity_x, velocity_y, on_ground