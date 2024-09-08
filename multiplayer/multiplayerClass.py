import pygame
import sys

pygame.init()

# Constants for the screen size
width = 800
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Traffic Road Rush')

# Colors
green = (1, 50, 30)
gray = (128, 128, 128)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0, 0)

def multiplayer():
    class Vehicle(pygame.sprite.Sprite):

        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)

            # scale the image so it fits in the lane
            image_scale = 45 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))

            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

    class PlayerVehicle(Vehicle):
        def __init__(self, x, y):
            image = pygame.image.load('../cars/AE86.png')
            super().__init__(image, x, y)

    # Player One
    playerOne_x = 220
    playerOne_y = 430

    # Player Two
    playerTwo_x = 580
    playerTwo_y = 430

    # create the player's car
    player_group = pygame.sprite.Group()
    player = PlayerVehicle(playerOne_x, playerOne_y)
    player2 = PlayerVehicle(playerTwo_x, playerTwo_y)
    player_group.add(player, player2)

    # Road class to handle drawing the road and markers
    class Road:
        def __init__(self):
            # Road dimensions and positions
            self.road_rect = pygame.Rect(50, 0, 350, height)
            self.left_edge_markers = pygame.Rect(50, 0, 10, height)
            self.right_edge_markers = pygame.Rect(390, 0, 10, height)

            # Lane marker positions
            self.markers_width = 10
            self.markers_height = 50
            self.lane_marker_move_y = 0

            # Lane positions
            self.left_lane = 100
            self.center_lane = 240
            self.right_lane = 324
            self.lanes = [self.left_lane, self.center_lane, self.right_lane]

            # Road animation speed
            self.speed = 2

        def draw(self, screen):
            # Draw the grass
            # screen.fill(green)

            # Draw the road
            pygame.draw.rect(screen, gray, self.road_rect)

            # Draw the road edges
            pygame.draw.rect(screen, white, self.left_edge_markers)
            pygame.draw.rect(screen, white, self.right_edge_markers)

            # Draw the lane markers (with movement to simulate driving)
            self.lane_marker_move_y += self.speed
            if self.lane_marker_move_y >= self.markers_height * 2:
                self.lane_marker_move_y = 0

            for y in range(-self.markers_height * 2, height, self.markers_height * 2):
                pygame.draw.rect(screen, yellow, (
                    self.left_lane + 45, y + self.lane_marker_move_y, self.markers_width, self.markers_height))
                pygame.draw.rect(screen, yellow, (
                    self.center_lane + 45, y + self.lane_marker_move_y, self.markers_width, self.markers_height))

    class RoadTwo:
        def __init__(self):
            self.road_rect = pygame.Rect(400, 0, 350, height)
            self.left_edge_markers = pygame.Rect(400, 0, 10, height)
            self.right_edge_markers = pygame.Rect(750, 0, 10, height)

            # Lane marker positions
            self.markers_width = 10
            self.markers_height = 50
            self.lane_marker_move_y = 0

            # Lane positions
            self.left_lane = 460
            self.center_lane = 590
            self.right_lane = 650
            self.lanes = [self.left_lane, self.center_lane, self.right_lane]

            # Road animation speed
            self.speed = 2

        def draw(self, screen):
            # Draw the grass
            # screen.fill(green)

            # Draw the road
            pygame.draw.rect(screen, gray, self.road_rect)

            # Draw the road edges
            pygame.draw.rect(screen, white, self.left_edge_markers)
            pygame.draw.rect(screen, white, self.right_edge_markers)

            # Draw the lane markers (with movement to simulate driving)
            self.lane_marker_move_y += self.speed
            if self.lane_marker_move_y >= self.markers_height * 2:
                self.lane_marker_move_y = 0

            for y in range(-self.markers_height * 2, height, self.markers_height * 2):
                pygame.draw.rect(screen, yellow, (
                    self.left_lane + 45, y + self.lane_marker_move_y, self.markers_width, self.markers_height))
                pygame.draw.rect(screen, yellow, (
                    self.center_lane + 45, y + self.lane_marker_move_y, self.markers_width, self.markers_height))

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    fps = 120

    # Create an instance of the Road class
    road_One = Road()
    road_Two = RoadTwo()

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # movement keys player One
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and player.rect.center[0] > road_One.left_lane:
                    player.rect.x -= 130
                elif event.key == pygame.K_d and player.rect.center[0] < road_One.right_lane:
                    player.rect.x += 130

                # player two
                if event.key == pygame.K_LEFT and player2.rect.center[0] > road_Two.left_lane:
                    player2.rect.x -= 130
                elif event.key == pygame.K_RIGHT and player2.rect.center[0] < road_Two.right_lane:
                    player2.rect.x += 130

        screen.fill(green)

        # Draw the road
        road_One.draw(screen)
        road_Two.draw(screen)

        # draw the players car
        player_group.draw(screen)

        # Update the display
        pygame.display.update()


multiplayer()