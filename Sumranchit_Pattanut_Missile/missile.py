from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

import math
import pygame

class Missile:
    def __init__(self, position, sprite_location):
        self.position = position
        self.storage_position = position

        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.STOP_DIST = 5

        self.timer = 0
        self.is_active = False

         # sprite
        self.sprite_image = image.load(sprite_location).convert_alpha()
        self.sprite_width = self.sprite_image.get_width()
        self.sprite_height = self.sprite_image.get_height()
        self.sprite_position = position - Vector2(self.sprite_image.get_width()/2, self.sprite_image.get_height()/2)

        self.first_shot_angle = 0
        self.sprite_rotation = 0
        self.rotated_image = 0

        self.gravity = Vector2(0,0)


    def missile_tracking(self, target_pos):
        MAX_FORCE = 5
        d = target_pos - self.position
        
        dist = d.length()

        if dist < self.STOP_DIST:
            self.reset_state()

        elif self.is_active == True:
            desired = d.normalize() * MAX_FORCE

            steering = desired - self.vel

            # set missile rotation
            self.sprite_rotation = 360 - self.calculate_angle(self.position, target_pos)
            
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)

            self.apply_force(steering)   

    def missile_nudge(self, target_pos):
        MAX_FORCE = 1
        d = target_pos - self.position
        
        dist = d.length()

        if dist < self.STOP_DIST:
            self.reset_state()

        elif self.is_active == True:
            desired = d.normalize() * MAX_FORCE * (dist / 5000)

            steering = desired

            # set missile rotation
            self.sprite_rotation = 360 - self.calculate_angle(self.position, target_pos)
            
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)

            self.apply_force(steering) 


    def go_straight(self):
        self.vel = self.first_shot_angle * 5
        self.sprite_rotation = 360 - self.calculate_angle(Vector2(0, 0), self.first_shot_angle)

    
    def missile_AI(self, target_pos):
        if self.is_active == True:
            self.timer += 1

            if self.timer > 150:
                self.missile_tracking(target_pos)
            elif self.timer > 50:
                self.missile_nudge(target_pos)
            else:
                self.go_straight()

    def apply_force(self, force):
        self.acc += force / self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity

    def enable_missile(self, shot_angle):
        self.is_active = True

        # change shot angle to vector
        angle_radians = math.radians(shot_angle)
        self.first_shot_angle = Vector2(math.cos(angle_radians), -math.sin(angle_radians))

    def reset_state(self):
        self.acc = Vector2(0,0)
        self.vel = Vector2(0,0)
        self.position = self.storage_position
        self.timer = 0
        self.is_active = False


    def calculate_angle(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1

        # Calculate the angle in radians using atan2
        angle_radians = math.atan2(dy, dx)

        # Convert the angle to degrees
        angle_degrees = math.degrees(angle_radians)

        # Ensure the angle is positive (0 to 360 degrees)
        if angle_degrees < 0:
            angle_degrees += 360

        return angle_degrees

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        if self.is_active == True:
            self.vel = self.vel + self.gravity

        self.position = self.position + self.vel
        self.acc = Vector2(0,0)

        # update rotation

        self.rotated_image = pygame.transform.rotate(self.sprite_image, self.sprite_rotation)

        self.sprite_position = self.position - Vector2(self.rotated_image.get_width()/2, self.rotated_image.get_height()/2)


    def draw(self, screen):
        screen.blit(self.rotated_image, self.sprite_position)