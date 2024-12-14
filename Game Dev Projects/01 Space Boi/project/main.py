import pygame
import math
import sys
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
def laser_update(laser_list, speed=300):
    for laser in laser_list:
        laser.y -= speed * delta_time
        if laser.bottom < 0:
            laser_list.remove(laser)

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
laser_surface = pygame.image.load(path+"images/projectiles/single_red1.png").convert_alpha()
laser_surface = pygame.transform.scale2x(laser_surface)
laser_list = []                                                                 

background_surface = pygame.image.load(path+"./images/background/background1.png").convert()
font = pygame.font.Font(path+"./fonts/subatomic.ttf", 50)
title_surface = font.render("Space Boi", True, "White")
title_rectangle = title_surface.get_rect(center=(WINDOW_WIDTH / 2, 150))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Player Methods # # # # 
x_speed = 0
y_speed = 0
move_speed = 7

# GAME LOOP
while True:
    # 1. Player Inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
    
    if event.type == pygame.JOYBUTTONDOWN:
        if pygame.joystick.Joystick(0).get_button(0) or pygame.joystick.Joystick(0).get_button(1):
            laser_rectangle = laser_surface.get_rect(midbottom = (ship_rectangle.midtop))
            laser_list.append(laser_rectangle)
            
    #Limiting Frame Rate
    delta_time = clock.tick(60) / 1000
    
    # Analog Stick
    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
    move(x_speed, y_speed)
    
    laser_update(laser_list)
    
    # 2. Updates
    display.fill((0, 0, 0))
    display.blit(background_surface, (0, 0))
    display.blit(ship_surface, ship_rectangle)
    for laser in laser_list:
        display.blit(laser_surface, laser)
    display.blit(title_surface, title_rectangle)
    
    # Draw custom Rectangles here
    pygame.draw.rect(display, "white", title_rectangle.inflate(50, 40), width=7, border_radius=5)
    
    # draw final frame
    pygame.display.update()