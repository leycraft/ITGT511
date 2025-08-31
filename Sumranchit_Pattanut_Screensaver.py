import pygame
from pygame.draw import circle, rect, polygon
from pygame.math import Vector2

window_width = 1270
window_height = 720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True


# shape 1: circle (red) --------------------------

circle_color = (255, 0, 0)
circle_radius = 100
circle_position = Vector2(window_width/2, window_height/2)

circle_vel = Vector2(0, 0)
circle_acc = Vector2(0, 0)

circle_acc.x = 1.5
circle_acc.y = 0.1

# shape 2: square (green) --------------------------

square_color = (0, 255, 0)
square_position = Vector2(window_width/8, window_height/8)
square_size = 100

square_vel = Vector2(0, 0)
square_acc = Vector2(0, 0)

square_acc.x = 3
square_acc.y = 3

# shape 3: triangle (blue) --------------------------

triangle_color = (0, 0, 255)
triangle_position = Vector2(window_width/2, window_height/8 * 7)
triangle_point_changing_increment = 1
triangle_point_range_x = 150
triangle_point_range_y = 50

triangle_vel = Vector2(0, 0)
triangle_acc = Vector2(0, 0)

triangle_acc.x = 0.2

# shape 4: bubble (light blue) --------------------------

bubble_color = (173, 216, 255)
bubble_radius = 20
bubble_radius_middle = 20
bubble_radius_safeguard = 10

bubble_grownth_rate = 0.5
bubble_grownth_acc = 0.01

bubble_position = Vector2(window_width/6, window_height/2)

bubble_vel = Vector2(0, 0)
bubble_acc = Vector2(0, 0)

bubble_acc.y = -1



# set up initial value, if any
# initial 1: for circle --------------------------

circle_vel.y = -6

# initial 2: for square --------------------------



# initial 3: for triangle --------------------------

triangle_vel.x = 10


# initial 4: for bubble --------------------------




# above only runs once ^
# below is a loop --------------------------
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    # shape 1: controlling circle --------------------------

    circle_vel = circle_vel + circle_acc
    circle_position = circle_position + circle_vel

    circle(screen, circle_color, circle_position, circle_radius)

    # maintain same x velocity

    circle_acc.x = 0

    # change y velocity for curve movement

    if circle_position.y >= window_height/2:
        circle_acc.y = -abs(circle_acc.y)
    else:
        circle_acc.y = abs(circle_acc.y)

    # bring circle back if it goes out of the window

    if circle_position.x >= window_width + circle_radius:
        circle_position.x = -circle_radius
    


    # shape 2: controlling square --------------------------

    square_vel = square_vel + square_acc
    square_position = square_position + square_vel

    square_object = pygame.Rect(square_position.x, square_position.y, square_size, square_size)
    rect(screen, square_color, square_object)

    # maintain velocity

    square_acc.x = 0
    square_acc.y = 0

    # change velocity if square knocks on corners

    if square_position.x >= window_width - square_size:
        square_vel.x = -abs(square_vel.x)
    elif square_position.x <= 0:
        square_vel.x = abs(square_vel.x)

    if square_position.y >= window_height - square_size:
        square_vel.y = -abs(square_vel.y)
    elif square_position.y <= 0:
        square_vel.y = abs(square_vel.y)

    # shape 3: controlling triangle --------------------------

    triangle_vel = triangle_vel + triangle_acc
    triangle_position = triangle_position + triangle_vel
    triangle_point1 = Vector2(triangle_position.x + triangle_point_range_x, triangle_position.y)
    triangle_point2 = Vector2(triangle_position.x, triangle_position.y + triangle_point_range_y)
    triangle_point3 = Vector2(triangle_position.x, triangle_position.y - triangle_point_range_y)

    polygon(screen, triangle_color, (triangle_point1, triangle_point2, triangle_point3))

    # change x velocity so triangle goes back and forth.

    if triangle_position.x >= window_width/2:
        triangle_acc.x = -abs(triangle_acc.x)
    else:
        triangle_acc.x = abs(triangle_acc.x)

    # change direction the triangle points to

    if triangle_vel.x >= 0:
        triangle_point_range_x = abs(triangle_point_range_x)
    else:
        triangle_point_range_x = -abs(triangle_point_range_x)


    # shape 4: controlling bubble --------------------------

    bubble_grownth_rate = bubble_grownth_rate + bubble_grownth_acc
    bubble_radius = bubble_radius + bubble_grownth_rate

    bubble_vel = bubble_vel + bubble_acc
    bubble_position = bubble_position + bubble_vel


    circle(screen, bubble_color, bubble_position, bubble_radius)


    # make bubble grows and shrinks

    if bubble_radius >= bubble_radius_middle:
        bubble_grownth_acc = -abs(bubble_grownth_acc)
    else:
        bubble_grownth_acc = abs(bubble_grownth_acc)

    # maintain bubble velocity

    bubble_acc.y = 0

    # make bubble loops back if it goes out of the screen

    if bubble_position.y < 0 - (bubble_radius + bubble_radius_safeguard):
        bubble_position.y =  window_height + (bubble_radius + bubble_radius_safeguard)



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()