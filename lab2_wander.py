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

        self.timer = 0
        
        self.agents = [
            Agent(position = Vector2(100, window_height/2), 
                          radius = 30, 
                          color = (100,0,0)),

            Agent(position = Vector2(500, window_height/2), 
                          radius = 20, 
                          color = (100,100,0)),

            Agent(position = Vector2(window_width/2, 300), 
                          radius = 10, 
                          color = (100,0,100))
        ]
        
        for agent in self.agents:
            agent.vel = Vector2(1,0)

        # waypoints system
        self.waypoints = [Vector2(200, 200), Vector2(1000, 200), Vector2(1000, 600), Vector2(200, 600)]

        self.current_waypoint_numbers = [0, 1, 2]
        self.targets = [self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[1]],
                        self.waypoints[self.current_waypoint_numbers[2]]]

        #self.target = Vector2(0, 0)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x, mouse_y)

    def update(self, delta_time_s):
        
        self.timer += delta_time_s

        for i, agent in enumerate(self.agents):
            target = agent.position + (agent.vel.normalize() * 100)

            if self.timer > 0.5:
                theta = random.randint(-100,100)
                target += Vector2(math.cos(theta), math.sin(theta)) * 50
            
            agent.seek_to(target)
            agent.update(delta_time_s)

        if self.timer > 0.5:
            self.timer = 0

        
    
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