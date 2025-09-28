from pygame.math import Vector2
from pygame.draw import circle, line, rect

class Agent:
    def __init__(self, position, radius, color):
        self.circle_color = color
        self.radius = radius
        self.position = position
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mass = 1.0
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5
        self.target = Vector2(0,0)
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2(0,0)

    def seek_to(self, target_pos):
        MAX_FORCE = 5
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
        MAX_FORCE = 5
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
        MAX_FORCE = 5
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
            d.scale_to_length(1)

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
            s.scale_to_length(1)
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
            s.scale_to_length(2)
            return s
        
        return Vector2(0,0)
            

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.position = self.position + self.vel
        self.vel *= 0.95
        self.acc = Vector2(0,0)

    def draw(self, screen):
        #circle(screen, "Yellow", self.position, self.EYE_SIGHT, width = 1)
        circle(screen, self.circle_color, self.position, self.radius)
        #circle(screen, "Green", self.position, self.STOP_DIST, width = 1)

        line(screen, (100,100,100), self.position, self.center_of_mass)