from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import math
import pygame
import copy

from pebble import Pebble

from fixed_limit_random import FixedLimit
from marblebag_random import MarbelBag
from predetermination_random import Predeterministic
from progressive_random import Progressive

from inventory_mineral import Inventory

class RockMining:
    def __init__(self, window_width, window_height):
        # screen size
        self.win_width = window_width
        self.win_height = window_height


        # random set up
        self.marblebag = MarbelBag()
        self.predetermination = Predeterministic()
        self.progressive = Progressive()


        # fixed limit is fused with progressive

        # marble
        self.minerals = ['silver', 'gold', 'diamond']
        self.minerals_probability = [6, 3, 1]

        self.marblebag.refill_specify(self.minerals, self.minerals_probability)

        # predetermination
        self.predetermination.set_random_rate(1, 3)

        # progressive
        self.progressive.set_random_rate(20, 10, 3)

        # gameplay variable
        self.cooldown_between_rock = 0
        self.inventory = [0, 0, 0]

        self.cooldown_between_mining = 0

        # inventory UI
        self.inventory_UI = Inventory(self.win_width, self.win_height)

        # sprites
        self.stone = image.load("sprites\\Stone.png").convert_alpha()
        self.stone_location = Vector2(self.win_width/2, self.win_height/2)

        self.iron_ingot = image.load("sprites\\Iron_Ingot.png").convert_alpha()
        self.gold_ingot = image.load("sprites\\Gold_Ingot.png").convert_alpha()
        self.diamond = image.load("sprites\\Diamond.png").convert_alpha()
        self.mineral_location = Vector2(self.win_width/2, self.win_height/2)
        self.original_mineral_location = copy.deepcopy(self.mineral_location)
        self.mineral_visible = False
        self.latest_mineral = ""
        self.min_vel = Vector2(0, 0)
        self.min_acc = Vector2(0, -0.1)

        self.pickaxe1 = image.load("sprites\\Diamond_Pickaxe.png").convert_alpha()
        self.pickaxe1_location = Vector2(self.win_width/2 + 150, self.win_height/2 - 150)
        self.pickaxe2 = image.load("sprites\\Diamond_Pickaxe2.png").convert_alpha()

        # pebble decoration
        self.pebbles = []
        for i in range(5):
            self.pebbles.append(Pebble(self.win_width, self.win_height))

        self.pebbles_extra = []
        for i in range(5):
            self.pebbles_extra.append(Pebble(self.win_width, self.win_height))


    def mine_rock(self):
        if(self.cooldown_between_rock == 0):
            if self.cooldown_between_mining == 0:
                mining_break = self.predetermination.draw()

                if mining_break == True:
                    if self.progressive.draw():
                        # get mineral in the stone
                        mineral_name = self.marblebag.draw(1)

                        if mineral_name == "silver":
                            self.inventory[0] += 1
                        elif mineral_name == "gold":
                            self.inventory[1] += 1
                        elif mineral_name == "diamond":
                            self.inventory[2] += 1

                        self.show_mineral(mineral_name)

                    else:
                        # the stone is empty
                        print("no mineral")

                    self.cooldown_between_rock = 120

                    for pebble in self.pebbles_extra:
                        pebble.start_pebble()

                    print(self.inventory)

                # things that happen even if the rock doesn't break

                self.cooldown_between_mining = 20
                for pebble in self.pebbles:
                    pebble.start_pebble()

                

        else:
            print("no rock to mine")

    def show_mineral(self, min_name):
        self.latest_mineral = min_name
        self.mineral_visible = True

    def reset_mineral(self):
        self.mineral_visible = False
        self.min_vel = Vector2(0,0)
        self.mineral_location = copy.deepcopy(self.original_mineral_location)

    def draw_mineral(self, screen, min_name, location):
        if min_name == "silver":
            self.create_sprite(screen, self.iron_ingot, location)
        elif min_name == "gold":
            self.create_sprite(screen, self.gold_ingot, location)
        elif min_name == "diamond":
            self.create_sprite(screen, self.diamond, location)

    def create_sprite(self, screen, image, location):
        image_width_offset = image.get_width()/2
        image_height_offset = image.get_height()/2

        new_location = Vector2(location.x - image_width_offset, location.y - image_height_offset)

        screen.blit(image, new_location)

    def update(self, delta_time_ms):
        if self.cooldown_between_rock > 0:
            self.cooldown_between_rock -= 1

        if self.cooldown_between_mining > 0:
            self.cooldown_between_mining -= 1

        for pebble in self.pebbles:
            pebble.update(delta_time_ms)

        for pebble in self.pebbles_extra:
            pebble.update(delta_time_ms)

        if self.mineral_visible:
            self.min_vel += self.min_acc
            self.mineral_location += self.min_vel

            if self.mineral_location.y < -100:
                self.reset_mineral()

        self.inventory_UI.update(delta_time_ms, self.inventory)

    def draw(self, screen):
        if self.cooldown_between_rock > 0:
            pass
        else:
            self.create_sprite(screen, self.stone, self.stone_location)

        if self.cooldown_between_mining > 0:
            self.create_sprite(screen, self.pickaxe2, self.pickaxe1_location)
        else:
            self.create_sprite(screen, self.pickaxe1, self.pickaxe1_location)

        for pebble in self.pebbles:
            pebble.draw(screen)

        for pebble in self.pebbles_extra:
            pebble.draw(screen)

        if self.mineral_visible:
            self.draw_mineral(screen, self.latest_mineral, self.mineral_location)

        self.inventory_UI.draw(screen)