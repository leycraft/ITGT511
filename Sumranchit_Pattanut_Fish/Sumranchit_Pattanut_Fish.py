#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from pygame import image
import random
import math

from fish import Fish
from food import Food

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

        # spawn fishes
        self.fishes = []

        for i in range(10):
            fish_insert = Fish(position = Vector2(random.randint(100, window_width), random.randint(100, window_height)))
            fish_insert.mass = 10
            self.fishes.append(fish_insert)

        # spawn food
        self.food_drop_point = Vector2(0, 0)

        self.food = []
        self.food_counter = 0

        for i in range(5):
            food_insert = Food(Vector2(-999, -999))
            self.food.append(food_insert)

        # castle obstuctcle
        self.castle_location = Vector2(window_width/2, 600)


        # decorations
        self.bg = "sprites\\water.png"
        self.castle = "sprites\\castle.png"

        self.bg_image = image.load(self.bg).convert_alpha()
        self.castle_image = image.load(self.castle).convert_alpha()



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.food[self.food_counter].enable_gravity == False:
                        self.food[self.food_counter].spawn_food(self.food_drop_point)

                        self.food_counter += 1
                        if self.food_counter >= len(self.food):
                            self.food_counter = 0


        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.food_drop_point = Vector2(mouse_x, mouse_y)

    def bound_check(self, agent):
        if agent.position.x < -10:
            agent.position.x = window_width + 30
        elif agent.position.x > window_width + 34:
            agent.position.x = -5

        if agent.position.y < -10:
            agent.position.y = window_height + 30
        elif agent.position.y > window_height + 34:
            agent.position.y = -5


    def update(self, delta_time_s):
        
        # fish ai everything
        for agent in self.fishes:
            cohesion_f = agent.get_cohesion_force(self.fishes)
            agent.apply_force(cohesion_f)

            separation_f = agent.get_separation_force(self.fishes)
            agent.apply_force(separation_f)

            align_f = agent.get_align_force(self.fishes)
            agent.apply_force(align_f)

            agent.flee_from(self.castle_location)

            agent.update(delta_time_s)
            
            for food in self.food:
                agent.find_food(food)

            self.bound_check(agent)

        # food physics
        for agent in self.food:
            agent.update(delta_time_s)

            # out of bound check
            if agent.position.y > window_height + 30:
                agent.reset_food()
        
    
    def draw(self):
        self.screen.blit(self.bg_image, Vector2(0,0))

        self.create_sprite(self.screen, self.castle_image, self.castle_location)

        for agent in self.fishes:
            agent.draw(self.screen)

        for agent in self.food:
            agent.draw(self.screen)

        circle(self.screen, "Red", self.food_drop_point, 20)

        pygame.display.flip()

    def create_sprite(self, screen, image, location):

        image_width_offset = image.get_width()/2
        image_height_offset = image.get_height()/2

        new_location = Vector2(location.x - image_width_offset, location.y - image_height_offset)

        screen.blit(image, new_location)
    

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