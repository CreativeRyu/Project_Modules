import pygame
import sys
path = "Game Dev Projects/01 Space Boi/"

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
ship_rectangle = ship_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
laser_surface = pygame.image.load(path+"images/projectiles/single_red1.png").convert_alpha()
laser_rectangle = laser_surface.get_rect(midbottom = (ship_rectangle.midtop))

background_surface = pygame.image.load(path+"./images/background/background1.png").convert()
font = pygame.font.Font(path+"./fonts/subatomic.ttf", 50)
titel_surface = font.render("Space Boi", True, "White")
titel_rectangle = titel_surface.get_rect(center=(WINDOW_WIDTH / 2, 150))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Player Methods # # # # 
x_speed = 0
y_speed = 0
move_speed = 4

def move(x_speed, y_speed):
    ship_rectangle.move_ip((x_speed * move_speed, y_speed * move_speed))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# GAME LOOP
while True:
    # 1. Player Inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        
    #Limiting Frame Rate
    clock.tick(60)
    
    # Analog Stick
    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
    move(x_speed, y_speed)
    
    laser_rectangle.y -= 7
    
    # 2. Updates
    display.fill((0, 0, 0))
    display.blit(background_surface, (0, 0))
    display.blit(ship_surface, ship_rectangle)
    display.blit(laser_surface, laser_rectangle)
    display.blit(titel_surface, titel_rectangle)
    
    # draw final frame
    pygame.display.update()