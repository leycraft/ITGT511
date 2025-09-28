#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
import random
import math

from agent import Agent

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
        
        self.agents = []

        for i in range(50):
            agent = Agent(position = Vector2(random.randint(100, window_width), random.randint(100, window_height)), 
                          radius = 10, 
                          color = (random.randint(50, 100),random.randint(50, 100),random.randint(50, 100)))
            agent.mass = 10
            self.agents.append(agent)



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x, mouse_y)

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
        
        for agent in self.agents:
            cohesion_f = agent.get_cohesion_force(self.agents)
            agent.apply_force(cohesion_f)

            separation_f = agent.get_separation_force(self.agents)
            agent.apply_force(separation_f)

            align_f = agent.get_align_force(self.agents)
            agent.apply_force(align_f)

            agent.update(delta_time_s)

            self.bound_check(agent)
        
    
    def draw(self):
        self.screen.fill("gray")

        for agent in self.agents:
            agent.draw(self.screen)

    

        pygame.display.flip()
    

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