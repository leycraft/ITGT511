from pygame.math import Vector2
from pygame.draw import circle, line, rect
from pygame import image

class Ant:
    def __init__(self, position, sprite_location):
        self.position = position
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.CAUTION_SIGHT = 200
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5

        self.carry_meat = False

        # sprite
        self.sprite_image = image.load(sprite_location).convert_alpha()
        self.sprite_width = self.sprite_image.get_width()
        self.sprite_height = self.sprite_image.get_height()
        self.sprite_position = position - Vector2(self.sprite_image.get_width()/2, self.sprite_image.get_height()/2)

        self.meat_carry = "sprites\\meat_cube.png"
        self.meat_carry_image = image.load(self.meat_carry).convert_alpha()

    def arrive_to(self, target_pos):
        MAX_FORCE = 3

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
        MAX_FORCE = 8
        d = -(target_pos - self.position)
        if d.length_squared() == 0:
            return
        
        dist = d.length()
        
        if dist < self.EYE_SIGHT:
            desired = d.normalize() * MAX_FORCE * ((self.EYE_SIGHT - dist) / self.EYE_SIGHT)
        else:
            desired = Vector2(0, 0)


        steering = desired - self.vel
        
        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)


    def be_cautious(self, predator_pos):
        MAX_FORCE = 5
        d = -(predator_pos - self.position)
        dist = d.length()

        if dist < self.CAUTION_SIGHT:
            desired = d.normalize() * MAX_FORCE * ((self.CAUTION_SIGHT - dist) / self.CAUTION_SIGHT)

            steering = desired
            
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)

            self.apply_force(steering)


    def Ant_AI_Full(self, target_pos, predator_pos):

        d = predator_pos - self.position
        dist = d.length()

        # try to avoid predator
        self.be_cautious(predator_pos)

        # if predator is close, run
        if dist < self.EYE_SIGHT:
            self.flee_from(predator_pos)

        # otherwise normal
        else:
            self.arrive_to(target_pos)


    def apply_force(self, force):
        self.acc += force / self.mass

    def carry_meat_state(self, is_carrying):
        self.carry_meat = is_carrying

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc = Vector2(0,0)

        self.sprite_position = self.position - Vector2(self.sprite_width/2, self.sprite_height/2)

    def draw(self, screen):
        circle(screen, "Red", self.position, self.EYE_SIGHT, width = 1)

        screen.blit(self.sprite_image, self.sprite_position)

        if self.carry_meat == True:
            screen.blit(self.meat_carry_image, self.position)

        circle(screen, "Green", self.position, self.STOP_DIST, width = 1)
        circle(screen, "Blue", self.position, self.CAUTION_SIGHT, width = 1)
