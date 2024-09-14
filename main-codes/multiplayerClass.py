import pygame
import random
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
            new_width = int(image.get_rect().width * image_scale)
            new_height = int(image.get_rect().height * image_scale)
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
    player_one = PlayerVehicle(playerOne_x, playerOne_y)
    player_two = PlayerVehicle(playerTwo_x, playerTwo_y)
    player_group.add(player_one, player_two)

    #speed
    speed_one = 2

    # create vehicles in road 1
    # load the vehicles
    image_filenames = ['car1.png', 'car3.jpg']
    vehicle_images = []
    for image_filename in image_filenames:
        image = pygame.image.load('../cars/' + image_filename)
        vehicle_images.append(image)

    # sprite group for vehicles
    vehicle_group_one = pygame.sprite.Group()
    vehicle_group_two = pygame.sprite.Group()

    # crash image
    crash = pygame.image.load('../utils/crash.png')
    crash_rect = crash.get_rect()



    # Road class to handle drawing the road and markers
    class RoadOne:
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
            self.speed = speed_one

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
            self.road_rect = pygame.Rect(400, 0, 360, height)
            self.left_edge_markers = pygame.Rect(400, 0, 10, height)
            self.right_edge_markers = pygame.Rect(750, 0, 10, height)

            # Lane marker positions
            self.markers_width = 10
            self.markers_height = 50
            self.lane_marker_move_y = 0

            # Lane positions
            self.left_lane = 460
            self.center_lane = 590
            self.right_lane = 700
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

    # add vehicles
    class Obstacle_RoadOne:
        def __init__(self):
            self.speed = speed_one
            self.score = 0
            self.lanes = [road_One.left_lane, road_One.center_lane, road_One.right_lane]
            self.player = player_one
            # add up to two vehicles
        def draw(self, screen):
            if len(vehicle_group_one) < 2:
                # ensure there's enough gap between vehicles
                add_vehicle = True
                for vehicle in vehicle_group_one:
                    if vehicle.rect.top < vehicle.rect.height:
                        add_vehicle = False

                if add_vehicle:
                    # select a random lane
                    lane = random.choice(self.lanes)

                    # select a random vehicle image
                    image = random.choice(vehicle_images)
                    vehicle = Vehicle(image, lane, height / -2)
                    vehicle_group_one.add(vehicle)

            for vehicle in vehicle_group_one:
                vehicle.rect.y += self.speed
                # remove the vehicle once it goes off screen
                if vehicle.rect.top >= height:
                    vehicle.kill()
                    # add to score
                    self.score += 1

                    #add speed to the game after passing 5 vehicles
                    if self.score > 0 and self.score % 5 == 0:
                        self.speed += 1
                        road_One.speed += 1

            # draw the vehicles on screen
            vehicle_group_one.draw(screen)

        #checks collision
        def check_collision(self):
            # Check for collision between player and any vehicle in vehicle_group_one
            if pygame.sprite.spritecollide(self.player, vehicle_group_one, False):
                # print("Collision detected!")
                road_One.speed = 0
                self.speed = 0

                # Display the crash image at the player's location
                crash_rect.center = self.player.rect.center
                screen.blit(crash, crash_rect)

                pygame.draw.rect(screen, black, (60, 50, 350, 100))

                font = pygame.font.Font(pygame.font.get_default_font(), 16)
                text = font.render('Game Over', True, white)
                text_rect = text.get_rect()
                text_rect.center = (220, 100)
                screen.blit(text, text_rect)

                return True

            return False

        def show_score(self):
            # display the score
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text_surf = font.render('Score: ' + str(self.score), True, black)
            text_rect = text_surf.get_rect()
            text_rect.center = (100, 50)
            screen.blit(text_surf, text_rect)


    class Obstacle_RoadTwo:
        def __init__(self):
            self.speed = 2
            self.score = 0
            self.lanes = [460, 580, 700]
            self.player = player_two
            # add up to two vehicles

        def draw(self, screen):
            if len(vehicle_group_two) < 2:
                # ensure there's enough gap between vehicles
                add_vehicle = True
                for vehicle in vehicle_group_two:
                    if vehicle.rect.top < vehicle.rect.height:
                        add_vehicle = False

                if add_vehicle:
                    # select a random lane
                    lane = random.choice(self.lanes)

                    # select a random vehicle image
                    image = random.choice(vehicle_images)
                    vehicle = Vehicle(image, lane, height / -2)
                    vehicle_group_two.add(vehicle)

            for vehicle in vehicle_group_two:
                vehicle.rect.y += self.speed
                # remove the vehicle once it goes off screen
                if vehicle.rect.top >= height:
                    vehicle.kill()

                    # add to score
                    self.score += 1

                    #add speed to the game after passing 5 vehicles
                    if self.score > 0 and self.score % 5 == 0:
                        self.speed += 1
                        road_Two.speed += 1

            # draw the vehicles on screen
            vehicle_group_two.draw(screen)

            # checks collision
        def check_collision(self):
            # Check for collision between player and any vehicle in vehicle_group_one
            if pygame.sprite.spritecollide(self.player, vehicle_group_two, False):
                # print("Collision detected!")
                road_Two.speed = 0
                self.speed = 0

                # Display the crash image at the player's location
                crash_rect.center = self.player.rect.center
                screen.blit(crash, crash_rect)

                pygame.draw.rect(screen, black, (390, 50, 360, 100))

                font = pygame.font.Font(pygame.font.get_default_font(), 16)
                text = font.render('Game Over', True, white)
                text_rect = text.get_rect()
                text_rect.center = (580, 100)
                screen.blit(text, text_rect)

                #result after crash
                # if player_one_active:
                #     if obstacles_two.score > obstacles_one.score:
                #         font = pygame.font.Font(pygame.font.get_default_font(), 16)
                #         text = font.render('Game Over', True, white)
                #         text_rect = text.get_rect()
                #         text_rect.center = (580, 200)
                #         screen.blit(text, text_rect)
                #         print('player 2 win')
                #     else:
                #         print('player 2 lose')
                # else:
                #     if obstacles_two.score > obstacles_one.score:
                #         font = pygame.font.Font(pygame.font.get_default_font(), 16)
                #         text = font.render('you win', True, white)
                #         text_rect = text.get_rect()
                #         text_rect.center = (580, 200)
                #         screen.blit(text, text_rect)
                #         print('player 2 win')
                #     else:
                #         print('player 2 lose')

                return True

            return False

        def show_score(self):
            # display the score
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text_surf = font.render('Score: ' + str(self.score), True, black)
            text_rect = text_surf.get_rect()
            text_rect.center = (500, 50)
            screen.blit(text_surf, text_rect)


    # Create an instance of the Road class
    # roadOne
    road_One = RoadOne()
    obstacles_one = Obstacle_RoadOne()
    road_Two = RoadTwo()
    obstacles_two = Obstacle_RoadTwo()

    # Main game loop
    running = True
    game_active = True
    gameOver = False
    player_one_active = True  # Player 1's state
    player_two_active = True  # Player 2's state
    clock = pygame.time.Clock()
    fps = 120

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # movement keys player One
            if player_one_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and player_one.rect.center[0] > road_One.left_lane:
                        player_one.rect.x -= 130
                    elif event.key == pygame.K_d and player_one.rect.center[0] < road_One.right_lane:
                        player_one.rect.x += 130

                # player two
            if player_two_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player_two.rect.center[0] > road_Two.left_lane:
                        player_two.rect.x -= 130
                    elif event.key == pygame.K_RIGHT and player_two.rect.center[0] < road_Two.right_lane:
                        player_two.rect.x += 130

        if game_active:
            screen.fill(green)

            # Draw the road
            road_One.draw(screen)
            obstacles_one.draw(screen)
            road_Two.draw(screen)
            obstacles_two.draw(screen)

            obstacles_one.show_score()
            obstacles_two.show_score()

            # draw the players car
            player_group.draw(screen)

            # Check for collision on road one
            # if (obstacles_one.check_collision() and obstacles_two.check_collision()) or (obstacles_two.check_collision() and obstacles_one.check_collision()):
            #     print(obstacles_one.show_score())
            #     print(obstacles_two.show_score())
            #     # Handle collision
            #     running = False
            if obstacles_one.check_collision():
                player_one_active = False


            if obstacles_two.check_collision():
                player_two_active = False

            if player_one_active == False and player_two_active == False:
                #screen.fill(green)
                gameOver = True

            if gameOver:
                screen.blit(crash, crash_rect)

                pygame.draw.rect(screen, black, (0, 0, width, height))

                font = pygame.font.Font(pygame.font.get_default_font(), 16)
                text = font.render('Game over. Play again? (Enter Y or N)', True, white)
                text_rect = text.get_rect()
                text_rect.center = (width / 2, 100)
                screen.blit(text, text_rect)

            pygame.display.update()

            while gameOver:
                clock.tick(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameOver = False
                        running = False

                    # check for player input
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            # reset the game
                            # gameOver = False
                            print('Yes')
                            multiplayer()
                            speed = 2
                            score = 0
                            # vehicle_group.empty()
                            # player.rect.center = [player_x, player_y]
                        elif event.key == pygame.K_n:
                            # exit the loop
                            print("No")
                            # gameOver = False
                            # game_active = False
                            score = 0
                            speed = 2
                            # running = False

            # Update the display
            pygame.display.update()

    #pygame.display.update()

# uncomment this when testing on the main.py
#multiplayer()