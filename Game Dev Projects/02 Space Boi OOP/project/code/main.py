import pygame
import sys
import math

path = "Game Dev Projects/02 Space Boi OOP/project"

class Ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(path+"/images/player/SmartSpaceShip.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.x_speed = 0
        self.y_speed = 0
        self.move_speed = 1.5
        self.can_fire = True
        self.last_laser_time = None
    
    def input_position(self):
        position = pygame.mouse.get_pos()
        self.rect.center = position
    
    def get_input(self):
        self.x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
        self.y_speed = round(pygame.joystick.Joystick(0).get_axis(1))

    def move(self):
        magnitude = math.sqrt(self.x_speed ** 2 + self.y_speed ** 2)
        
        if magnitude != 0:
            normalized_x = self.x_speed / magnitude
            normalized_y = self.y_speed / magnitude
        else:
            normalized_x, normalized_y = 0, 0
            
        self.rect.move_ip(normalized_x * self.move_speed, normalized_y * self.move_speed)
    
    def fire_laser(self):
        if (pygame.joystick.Joystick(0).get_button(0) or pygame.joystick.Joystick(0).get_button(1)) and self.can_fire:
            Laser(laser_group, self.rect.midtop)
            self.can_fire = False
            self.last_laser_time = pygame.time.get_ticks()
    
    def laser_cooldown(self):
        if not self.can_fire:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_laser_time >= 500:
                self.can_fire = True
    
    def update(self):
        self.get_input()
        self.move()
        self.fire_laser()
        self.laser_cooldown()

class Laser(pygame.sprite.Sprite):
    def __init__(self, group, init_position):
        super().__init__(group)
        self.image = pygame.image.load(path+"/images/projectiles/single_blue2.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(midbottom = (init_position))
        self.rect.centery += 45                                               
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 500
    
    def update(self):
        self.position += self.direction * self.speed * delta_time
        self.rect.topleft = (round(self.position.x), round(self.position.y))

# # # # Pygame Init Part # # # # 
pygame.init()
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Boi")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Get Gamepads and Joysticks here
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Background # # # # 
bg_surface = pygame.image.load(path+"/images/background/background2.png").convert()

# # # # Sprite Groups # # # # 
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()  

# # # # Object Init # # # # 
spaceship = Ship(spaceship_group)

# GAME LOOP
while True:
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
    
    # Delta Time
    delta_time = clock.tick() / 1000
    
    # Background
    display_surface.blit(bg_surface, (0, 0))
    
    # Update
    spaceship_group.update()
    laser_group.update()
    
    # Graphic Drawing
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)

    # draw final frame
    pygame.display.update()