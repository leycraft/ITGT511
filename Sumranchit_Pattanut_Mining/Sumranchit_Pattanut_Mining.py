import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from pygame import image
import random
import math

random_seed = 1
random.seed(random_seed)

from rock_mining import RockMining

window_width = 1280
window_height = 720

class App:
    def __init__(self):
        print("Application is created.")
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.CHANGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHANGE_DIR, 2000)
        self.running = True

        self.rock_miner = RockMining(window_width, window_height)

        # sprites
        self.bg = image.load("sprites\\Minecraft_Cave.png").convert_alpha()
        self.bg_location = Vector2(window_width/2, window_height/2)



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.rock_miner.mine_rock()

        mouse_x, mouse_y = pygame.mouse.get_pos()

    def update(self, delta_time_s):
        self.rock_miner.update(delta_time_s)
        
    
    def draw(self):
        self.screen.fill("gray")
        self.create_sprite(self.screen, self.bg, self.bg_location)

        self.rock_miner.draw(self.screen)

        pygame.display.flip()

    def create_sprite(self, screen, image, location):
        image_width_offset = image.get_width()/2
        image_height_offset = image.get_height()/2

        new_location = Vector2(location.x - image_width_offset, location.y - image_height_offset)

        screen.blit(image, new_location)
    

    # don't mess below this line ----------------------------------

    def run(self):
        while self.running:
            dt = self.clock.tick(60)/1000
            self.handle_input()
            self.update(dt)
            self.draw()
            

        pygame.quit()


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()