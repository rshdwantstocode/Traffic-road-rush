import pygame
import sys

pygame.init()

width = 800
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Traffic Road Rush')

# Road 1
# game color
green = (1, 50, 30)
gray = (128,128,128)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0,0)

# markers size
markers_width = 10
markers_height = 50

# road edge and markers
road = (50, 0, 350, height)
left_edge_markers = (50, 0, markers_width, height)
right_edge_markers = (390, 0, markers_width, height)

# x coordinates of lane
left_lane = 76
center_lane = 76
right_lane = 76
lanes = [left_lane, center_lane, right_lane]

# animation movement
lane_marker_move_y = 0

#game loop
running = True
clock = pygame.time.Clock()
fps = 60

while running:
    clock.tick(fps)

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