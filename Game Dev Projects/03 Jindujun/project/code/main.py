import pygame
import sys
import time
from settings import *

class Game:
    def __init__(self):
        
        # Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Jindujun")
        self.clock = pygame.time.Clock()
    
    def run(self):
        last_time = time.time()
        while True:
            
            # Delta Time
            delta_time = time.time() - last_time
            last_time = time.time()
            
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Game Logic
            pygame.display.update()
            self.clock.tick(FRAMERATE)
            
    
if __name__ == "__main__":
    game = Game()
    game.run()