import pygame
import sys


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

# x coordinates of lane
left_lane = 280
center_lane = 420
right_lane = 550
lane = [left_lane, center_lane, right_lane]

# animation movement
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        #scale the image so it fits in the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('cars/AE86.png')
        super().__init__(image, x, y)

# Player's starting coordinates
player_x = 400
player_y = 430

# create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)


# game settings
gameover = False
speed = 2
score = 0

# game loop
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # move the players car using left/right arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 130
            elif event.key == pygame.K_RIGHT and player.rect.center[1] < right_lane:
                player.rect.x += 130


    # draw grass
    screen.fill(green)

    # draw the road
    pygame.draw.rect(screen, gray, road)

    # road edges
    pygame.draw.rect(screen, white, left_edge_markers)
    pygame.draw.rect(screen, white, right_edge_markers)

    # lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= markers_height * 2:
        lane_marker_move_y = 0
    for y in range(markers_height * -2, height, markers_height * 2):
        pygame.draw.rect(screen, yellow, (left_lane + 45, y + lane_marker_move_y, markers_width, markers_height))
        pygame.draw.rect(screen, yellow, (center_lane + 45, y + lane_marker_move_y, markers_width, markers_height))

    # draw the players car
    player_group.draw(screen)

    pygame.display.update()
    clock.tick(60)