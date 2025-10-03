from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import pygame

class Food:
    def __init__(self, position):
        self.position = position
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.STOP_DIST = 5
        self.gravity = Vector2(0, 0.1)
        self.center_of_mass = Vector2(0,0)

        self.storage_position = self.position

        self.enable_gravity = False

        # sprite
        self.sprite_location = "sprites\\food.png"

        self.sprite_image = image.load(self.sprite_location).convert_alpha()
        self.sprite_width = self.sprite_image.get_width()
        self.sprite_height = self.sprite_image.get_height()
        self.sprite_position = self.position - Vector2(self.sprite_width/2, self.sprite_height/2)

    def reset_food(self):
        self.position = self.storage_position
        self.enable_gravity = False
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    def spawn_food(self, position):
        self.enable_gravity = True
        self.position = position


    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        if self.enable_gravity == True:
            self.vel += self.gravity
        self.position = self.position + self.vel
        self.vel *= 0.95
        self.acc = Vector2(0,0)

        self.sprite_position = self.position - Vector2(self.sprite_width/2, self.sprite_height/2)

        # out of bound check

    def draw(self, screen):
        screen.blit(self.sprite_image, self.sprite_position)