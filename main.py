import sys
import pygame


pygame.init()
# 800x480 5 inch rpi screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Traffic Road Rush')
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((94, 129, 162))

    pygame.display.update()
    clock.tick(60)