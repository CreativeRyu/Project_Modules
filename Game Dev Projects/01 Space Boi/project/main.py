import pygame
import math
import sys
from random import randint
path = "Game Dev Projects/01 Space Boi/project/"

# Move Methode für die Spielfigur
def move(x_speed, y_speed):
    magnitude = math.sqrt(x_speed ** 2 + y_speed ** 2)
    
    if magnitude != 0:
        normalized_x = x_speed / magnitude
        normalized_y = y_speed / magnitude
    else:
        normalized_x, normalized_y = 0, 0
    
    ship_rectangle.move_ip(normalized_x * move_speed, normalized_y * move_speed)

# Bewegung der Laser zum oberen Bildschirmrand
def laser_update(laser_list, speed=400):
    for laser in laser_list:
        laser.y -= speed * delta_time
        if laser.bottom < 0:
            laser_list.remove(laser)

# Cooldown Timer für den Laser
def laser_cooldown(can_fire, duration= 500):
    if not can_fire: 
        current_time = pygame.time.get_ticks()
        if current_time - last_laser_time >= duration:
            can_fire = True
    return can_fire

def asteroid_behaviour(asteroid_list, speed=300):
    for asteroid in asteroid_list:
        asteroid.y += speed * delta_time
        if asteroid.top >= WINDOW_HEIGHT:
            asteroid_list.remove(asteroid)
    
def display_score():
    score = f"Score: {pygame.time.get_ticks() // 1000}"
    score_surface = font_score.render(score, True, "White")
    score_rect = score_surface.get_rect(midtop = (120, WINDOW_HEIGHT - 60))
    display.blit(score_surface, score_rect)  
    display.blit(title_surface, title_rectangle)
    pygame.draw.rect(display, "white", title_rectangle.inflate(50, 40), width=7, border_radius=5)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Pygame Init Part # # # # 
pygame.init()

# Get Gamepads and Joysticks here
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Import Images # # # # 
ship_surface = pygame.image.load(path+"images/player/SmartSpaceShip.png").convert_alpha()
ship_surface = pygame.transform.scale2x(ship_surface)
ship_rectangle = ship_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
laser_surface = pygame.image.load(path+"images/projectiles/single_blue1.png").convert_alpha()
laser_surface = pygame.transform.scale2x(laser_surface)
laser_list = []
asteroid_surface = pygame.image.load(path+"images/enemy/Asteroid L lv 1.png").convert_alpha()
asteroid_surface = pygame.transform.scale2x(asteroid_surface)
asteroid_list = []                                                  

# Import Text
background_surface = pygame.image.load(path+"./images/background/background1.png").convert()
font = pygame.font.Font(path+"./fonts/subatomic.ttf", 50)
font_score = pygame.font.Font(path+"fonts/subatomic.ttf", 30)
title_surface = font.render("Space Boi", True, "White")
title_rectangle = title_surface.get_rect(center=(WINDOW_WIDTH / 2, 150))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Player Variables # # # # 
x_speed = 0
y_speed = 0
move_speed = 7
can_fire = True
last_laser_time = None
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 1000)    

# GAME LOOP
while True:
    # 1. Player Inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
    
        if event.type == pygame.JOYBUTTONDOWN and can_fire:
            if pygame.joystick.Joystick(0).get_button(0) or pygame.joystick.Joystick(0).get_button(1):
                
                # Laser Logic
                laser_rectangle = laser_surface.get_rect(midbottom = (ship_rectangle.midtop))
                laser_rectangle.centery += 30
                laser_list.append(laser_rectangle)
                
                # Laser Timer
                can_fire = False
                last_laser_time = pygame.time.get_ticks()
        
        x_position = randint(-100, WINDOW_WIDTH + 100)
        y_position = randint(-100, -50)
        if event.type == asteroid_timer: 
            asteroid_rectangle = asteroid_surface.get_rect(center = (x_position, y_position))
            asteroid_list.append(asteroid_rectangle)
                    
    #Limiting Frame Rate
    delta_time = clock.tick(60) / 1000
    
    # Analog Stick
    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
    move(x_speed, y_speed)
    
    # Laser Updates
    laser_update(laser_list)
    can_fire = laser_cooldown(can_fire, 400)
    
    # Asteroid Update
    asteroid_behaviour(asteroid_list)
    
    # drawings
    display.fill((0, 0, 0))
    display.blit(background_surface, (0, 0))
    display.blit(ship_surface, ship_rectangle)
    for laser in laser_list:
        display.blit(laser_surface, laser)

    for asteroid in asteroid_list:
        display.blit(asteroid_surface, asteroid)
    
    display_score()
    
    # draw final frame
    pygame.display.update()