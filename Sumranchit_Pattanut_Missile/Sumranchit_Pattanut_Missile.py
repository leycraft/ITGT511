#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from pygame import image
import random
import math

from missile import Missile

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

        self.missile_position = Vector2(window_width/2, 600)

        
        self.missiles = [
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png"),
            Missile(position = self.missile_position, 
                    sprite_location = "sprites\\missile.png")
        ]

        for missile in self.missiles:
            missile.set_gravity(Vector2(0, 0.1))

        self.target = Vector2(0, 0)

        self.missile_counter = 0

        self.barrel = "sprites\\barrel.png"
        self.barrel_image = image.load(self.barrel).convert_alpha()
        self.barrel_rect = self.barrel_image.get_rect(center = self.missile_position)
        self.barrel_rotation = 0
        self.barrel_rotation_increment = 0.5

        self.rotated_barrel = 0

        # decorations
        self.bg = "sprites\\sky.png"
        self.dome = "sprites\\dome.png"

        self.bg_image = image.load(self.bg).convert_alpha()
        self.dome_image = image.load(self.dome).convert_alpha()



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.missiles[self.missile_counter].is_active == False:
                        self.missiles[self.missile_counter].enable_missile(self.barrel_rotation)

                    
                        self.missile_counter += 1
                        if self.missile_counter >= len(self.missiles):
                            self.missile_counter = 0


        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target = Vector2(mouse_x, mouse_y)

    def update(self, delta_time_s):

        for missile in self.missiles:
            missile.missile_AI(self.target)
            missile.update(delta_time_s)

        # barrel rotation
        self.rotated_barrel = pygame.transform.rotate(self.barrel_image, self.barrel_rotation)
        self.barrel_rect = self.rotated_barrel.get_rect(center = self.missile_position)

        self.barrel_rotation += self.barrel_rotation_increment

        if self.barrel_rotation > 180:
            self.barrel_rotation_increment = -abs(self.barrel_rotation_increment)
        elif self.barrel_rotation < 0:
            self.barrel_rotation_increment = abs(self.barrel_rotation_increment)

    
    def draw(self):
        self.screen.fill("gray")

        self.screen.blit(self.bg_image, Vector2(0,0))

        for missile in self.missiles:
            missile.draw(self.screen)

        

        self.screen.blit(self.rotated_barrel, self.barrel_rect)

        self.screen.blit(self.dome_image, Vector2(window_width/2 - (self.dome_image.get_width() / 2), 500))

        circle(self.screen, "Red", self.target, 20)

        pygame.display.flip()
    

    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.handle_input()
            self.update(dt)
            self.draw()
            

        pygame.quit()


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()