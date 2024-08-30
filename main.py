import sys
import pygame


pygame.init()
# 800x480 5 inch rpi screen
width = 800
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Traffic Road Rush')

# game color
green = (1, 50, 30)
gray = (128,128,128)
yellow = (255,255,0)
white = (255,255,255)

# markers size
markers_width = 10
markers_height = 50

# road edge and markers
road = (200, 0, 400, height)
left_edge_markers = (195, 0, markers_width, height)
right_edge_markers = (595, 0, markers_width, height)

# game loop
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw grass
    screen.fill(green)

    # draw the road
    pygame.draw.rect(screen, gray, road)

    # road edges
    pygame.draw.rect(screen, white, left_edge_markers)
    pygame.draw.rect(screen, white, right_edge_markers)

    pygame.display.update()
    clock.tick(60)