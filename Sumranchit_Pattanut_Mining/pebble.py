from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import math
import pygame
import copy
import random

class Pebble:
    def __init__(self, window_width, window_height):
        # screen size
        self.win_width = window_width
        self.win_height = window_height

        self.pebble = image.load("sprites\\pebble.png").convert_alpha()
        self.pebble_location = Vector2(self.win_width/2, self.win_height/2)
        self.original_pebble_location = copy.deepcopy(self.pebble_location)
        self.pebble_visible = False

        self.pebble_vel = Vector2(0, 0)
        self.pebble_gravity = Vector2(0, 0.3)

    def start_pebble(self):
        self.pebble_visible = True

        random_x = random.uniform(-5, 5)
        random_y = random.uniform(-1, -5)

        self.pebble_vel = Vector2(random_x, random_y)

    def reset_pebble(self):
        self.pebble_visible = False
        self.pebble_location = copy.deepcopy(self.original_pebble_location)
        self.pebble_vel = Vector2(0, 0)

    def create_sprite(self, screen, image, location):
        image_width_offset = image.get_width()/2
        image_height_offset = image.get_height()/2

        new_location = Vector2(location.x - image_width_offset, location.y - image_height_offset)

        screen.blit(image, new_location)

    def update(self, delta_time_ms):
        if self.pebble_visible:
            self.pebble_vel += self.pebble_gravity
            self.pebble_location += self.pebble_vel

            if(self.pebble_location.y > self.win_height + 50):
                self.reset_pebble()

    def draw(self, screen):
        if self.pebble_visible:
            self.create_sprite(screen, self.pebble, self.pebble_location)