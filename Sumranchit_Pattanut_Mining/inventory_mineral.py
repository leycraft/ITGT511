from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import math
import pygame
import copy
import random

class Inventory:
    def __init__(self, window_width, window_height):
        # screen size
        self.win_width = window_width
        self.win_height = window_height

        self.inventory = [0,0,0]

        # sprite
        self.silver = image.load("sprites\\Iron_Ingot_small.png").convert_alpha()
        self.silver_location = Vector2(50, self.win_height - 50)

        self.gold = image.load("sprites\\Gold_Ingot_small.png").convert_alpha()
        self.gold_location = Vector2(50, self.win_height - 100)

        self.diamond = image.load("sprites\\Diamond_small.png").convert_alpha()
        self.diamond_location = Vector2(50, self.win_height - 150)

        self.UI_increment = 50


    def create_sprite(self, screen, image, location):
        image_width_offset = image.get_width()/2
        image_height_offset = image.get_height()/2

        new_location = Vector2(location.x - image_width_offset, location.y - image_height_offset)

        screen.blit(image, new_location)

    def update(self, delta_time_ms, inventory_data):
        self.inventory = inventory_data

    def draw(self, screen):
        for i in range(self.inventory[0]):
            location = Vector2(self.silver_location.x + (i * self.UI_increment), self.silver_location.y)
            self.create_sprite(screen, self.silver, location)

        for i in range(self.inventory[1]):
            location = Vector2(self.gold_location.x + (i * self.UI_increment), self.gold_location.y)
            self.create_sprite(screen, self.gold, location)

        for i in range(self.inventory[2]):
            location = Vector2(self.diamond_location.x + (i * self.UI_increment), self.diamond_location.y)
            self.create_sprite(screen, self.diamond, location)