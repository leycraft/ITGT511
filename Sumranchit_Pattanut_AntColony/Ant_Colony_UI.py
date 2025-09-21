#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from pygame import image
import pygame_gui

from ant import Ant

window_width = 1280
window_height = 720

class App:
    def __init__(self):
        print("Application is created.")
        pygame.init()

        self.screen = pygame.display.set_mode((window_width, window_height))

        self.manager = pygame_gui.UIManager((800, 600))
        self.hello_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((350, 275), (100, 50)), 
                                                         text = "say hello", 
                                                         manager = self.manager)
        #self.horizontal_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect = pygame.Rect((150, 175), (300, 50)), 
        #                                                                start_value=0,
        #                                                                value_range=(0,100),
        #                                                                manager=self.manager)


        self.clock = pygame.time.Clock()
        self.CHANGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHANGE_DIR, 2000)
        self.running = True
        
        self.ants = [
            Ant(position = Vector2(100, window_height/2), 
                          sprite_location = "sprites\\ant_head_r.png"),

            Ant(position = Vector2(500, window_height/2), 
                          sprite_location = "sprites\\ant_head_g.png"),

            Ant(position = Vector2(window_width/2, 300), 
                          sprite_location = "sprites\\ant_head_b.png")
        ]
        

        # waypoints system
        self.waypoints = [Vector2(100, 600), Vector2(1100, 100)]

        self.current_waypoint_numbers = [1, 1, 1]
        self.targets = [self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[1]],
                        self.waypoints[self.current_waypoint_numbers[2]]]

        # predator object
        self.predator = Vector2(0, 0)

        # decorations
        self.bg = "sprites\\sand_floor.png"
        self.ant_cave = "sprites\\cave.png"
        self.meat = "sprites\\meat.png"

        self.bg_image = image.load(self.bg).convert_alpha()
        self.ant_cave_image = image.load(self.ant_cave).convert_alpha()
        self.meat_image = image.load(self.meat).convert_alpha()


    def handle_input(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                #event.ui_element == pygame_gui.UI_BUTTON_PRESSED:
                print("hello world")

            self.manager.process_events(event)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.predator = Vector2(mouse_x, mouse_y)

    def update(self, delta_time_ms):
        for i, ant in enumerate(self.ants):
            dist = (ant.position - self.targets[i]).length()
            if dist < ant.STOP_DIST:
                # reach destination

                self.current_waypoint_numbers[i] += 1
                if self.current_waypoint_numbers[i] >= len(self.waypoints):
                    self.current_waypoint_numbers[i] = 0

                # check if going to carry meat
                # 0 is home. go home = carry meat
                # 1 is meat. 
                if self.current_waypoint_numbers[i] == 0:
                    ant.carry_meat_state(True)
                else:
                    ant.carry_meat_state(False)

                self.targets[i] = self.waypoints[self.current_waypoint_numbers[i]]

            ant.Ant_AI_Full(self.targets[i], self.predator)

            self.manager.update(delta_time_ms)
            ant.update(delta_time_ms)

        
    
    def draw(self):
        self.screen.blit(self.bg_image, Vector2(0,0))
        self.screen.blit(self.ant_cave_image, Vector2(50,500))
        self.screen.blit(self.meat_image, Vector2(950,10))

        for ant in self.ants:
            ant.draw(self.screen)

        self.manager.draw_ui(self.screen)

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