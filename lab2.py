#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

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

        self.ball = Agent(position = Vector2(window_width/2, window_height/2), 
                          radius = 100, 
                          color = (100,0,0))
        
        self.target = Vector2(0, 0)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target = Vector2(mouse_x, mouse_y)

    def update(self, delta_time_ms):
        self.ball.seek_to(self.target)
        self.ball.update(delta_time_ms)
        
    
    def draw(self):
        self.screen.fill("gray")
        self.ball.draw(self.screen)
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