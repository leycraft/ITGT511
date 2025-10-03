from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import pygame
import random
import food

class Fish:
    def __init__(self, position):
        self.position = position
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.CAUTION_SIGHT = 200
        self.EYE_SIGHT = 250
        self.STOP_DIST = 25
        self.target = Vector2(0,0)
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2(0,0)

        self.hunger_timer = random.randint(300, 600)

        # sprite
        self.sprite_location = "sprites\\gold_fish.png"
        self.sprite_hungry_location = "sprites\\gold_fish_hungry.png"

        self.sprite_image = image.load(self.sprite_location).convert_alpha()
        self.sprite_image_hungry = image.load(self.sprite_hungry_location).convert_alpha()

        self.sprite_width = self.sprite_image.get_width()
        self.sprite_height = self.sprite_image.get_height()
        self.sprite_position = self.position - Vector2(self.sprite_width/2, self.sprite_height/2)

        self.sprite_image_flip = pygame.transform.flip(self.sprite_image, True, False)
        self.sprite_image_hungry_flip = pygame.transform.flip(self.sprite_image_hungry, True, False)
        


    def seek_to(self, target_pos):
        MAX_FORCE = 7
        self.target = target_pos
        
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)

    def arrive_to(self, target_pos):
        MAX_FORCE = 10
        self.target = target_pos

        d = target_pos - self.position
            
        if d.length_squared() == 0:
            return
        
        dist = d.length()

        if dist < self.STOP_DIST:
            desired = Vector2(0, 0)

        elif dist < self.EYE_SIGHT:
            desired = d.normalize() * MAX_FORCE * (dist / self.EYE_SIGHT)
        else:
            desired = d.normalize() * MAX_FORCE

        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)        

    def flee_from(self, target_pos):
        MAX_FORCE = 10
        d = -(target_pos - self.position)
        if d.length_squared() == 0:
            return
        
        dist = d.length()
        
        if dist < self.EYE_SIGHT:
            desired = d.normalize() * MAX_FORCE * ((self.EYE_SIGHT - dist + 100) / self.EYE_SIGHT)
        else:
            desired = Vector2(0, 0)


        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force / self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, agents):
        center_of_mass = Vector2(0,0)
        count = 0

        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if 0 < dist < 400*400 :
                center_of_mass += agent.position
                count += 1

        if count > 0:
            center_of_mass /= count

            d = center_of_mass - self.position
            d.scale_to_length(0.7)

            self.center_of_mass = center_of_mass

            return d
        return Vector2()
    
    def get_separation_force(self, agents):
        s = Vector2(0,0)
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()

            if dist < 100*100 and dist != 0:
                d =  self.position - agent.position
                s += d
                count += 1

        if count > 0:
            s.scale_to_length(2)
            return s
        
        return Vector2(0,0)
    
    def get_align_force(self, agents):
        s = Vector2(0,0)
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()

            if dist < 500*500 and dist != 0:
                d =  self.position - agent.position
                s += agent.vel
                count += 1

        if count > 0 and s != Vector2():
            s /= count
            s.scale_to_length(1)
            return s
        
        return Vector2(0,0)
    
    def find_food(self, target):
        # check hunger and object type
        if self.hunger_timer == 0 and type(target) == food.Food:
            dist = (target.position - self.position).length()

            if dist <= self.EYE_SIGHT:
                self.seek_to(target.position)

                if dist <= self.STOP_DIST:
                    self.hunger_timer = random.randint(300, 600)
                    target.reset_food()
    
    def be_cautious(self, predator_pos):
        MAX_FORCE = 5
        d = -(predator_pos - self.position)
        dist = d.length()

        if dist < self.CAUTION_SIGHT:
            desired = d.normalize() * MAX_FORCE * ((self.CAUTION_SIGHT - dist + 100) / self.CAUTION_SIGHT)

            steering = desired
            
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)

            self.apply_force(steering)

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.position = self.position + self.vel
        self.vel *= 0.95
        self.acc = Vector2(0,0)

        self.sprite_position = self.position - Vector2(self.sprite_width/2, self.sprite_height/2)

        if self.hunger_timer > 0:
            self.hunger_timer -= 1

    def draw(self, screen):
        if self.vel.x >= 0:
            if self.hunger_timer == 0:
                screen.blit(self.sprite_image_hungry, self.sprite_position)
            else:
                screen.blit(self.sprite_image, self.sprite_position)
        else:
            if self.hunger_timer == 0:
                screen.blit(self.sprite_image_hungry_flip, self.sprite_position)
            else:
                screen.blit(self.sprite_image_flip, self.sprite_position)
        
        
        #line(screen, (100,100,100), self.position, self.center_of_mass)

        #circle(screen, "Green", self.position, self.CAUTION_SIGHT, width = 1)
        #circle(screen, "Red", self.position, self.EYE_SIGHT, width = 1)
        #circle(screen, "Blue", self.position, self.STOP_DIST, width = 1)