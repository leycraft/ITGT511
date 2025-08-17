#lab1
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

window_width = 1280
window_height = 720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True

circle_color = (255, 0, 0)
radius = 100
position = Vector2(window_width/2, window_height/2)
vel = Vector2(0, 0)
acc = Vector2(0, 0)

acc.x = 1
acc.y = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    # RENDER YOUR GAME HERE

    vel = acc
    position = position + vel

    circle(screen, circle_color, position, radius)

    acc.x = 0
    acc.y = 0

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()