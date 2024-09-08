import pygame
import random
import sys
# from multiplayer.multiplayerClass import multiplayer

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
black = (0,0,0,0)

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
right_lane = 500
lanes = [left_lane, center_lane, right_lane]

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

#text in main menu
title_font = pygame.font.Font('font/Pixeltype.ttf', 60)
space_font = pygame.font.Font('font/Pixeltype.ttf', 40)
main_text = title_font.render('Traffic Road Rush', False, white)
main_text_rect = main_text.get_rect(center=(400, 100))

space_text = space_font.render('Press "SPACE" to start the game', False, white)
space_text_rect = space_text.get_rect(center=(400, 300))
alpha_value = 0  # Starting transparency (0 = fully transparent)
fade_in = True
def animationMenu():
    global alpha_value, fade_in
    if fade_in:
        alpha_value += 10  # Increase alpha to fade in
        if alpha_value >= 255:  # Fully opaque, start fading out
            alpha_value = 255
            fade_in = False
    else:
        alpha_value -= 10  # Decrease alpha to fade out
        if alpha_value <= 0:  # Fully transparent, start fading in
            alpha_value = 0
            fade_in = True

    # Apply alpha to the space text surface
    space_text.set_alpha(alpha_value)

# Player's starting coordinates
player_x = 400
player_y = 430

# create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

#load the vehicles
image_filenames = ['car1.png', 'car3.jpg']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('cars/'+ image_filename)
    vehicle_images.append(image)

#sprite group for vehicles
vehicle_group = pygame.sprite.Group()

# crash image
crash = pygame.image.load('utils/crash.png')
crash_rect = crash.get_rect()


# game settings
gameover = False
speed = 2
score = 0

# game loop
clock = pygame.time.Clock()
fps = 120
game_active = False
multiplayer_active = False
running = True


while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # move the players car using left/right arrow keys
        #check if the game is active before activating the keys
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.rect.center[0] > left_lane:
                    player.rect.x -= 130
                elif event.key == pygame.K_RIGHT and player.rect.center[0] < right_lane:
                    player.rect.x += 130
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                multiplayer_active = True

            # check if there's a sideswipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    #place the player's car next to the other vehicle
                    #and determine where to position the crash image
                    if event.key == pygame.K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == pygame.K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    if game_active:
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

        #add up to two vehicles
        if len(vehicle_group) < 2:

            #ensure there's enough gap between vehicles
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height:
                    add_vehicle = False

            if add_vehicle:

                #select a random lane
                lane = random.choice(lanes)

                #select a random vehicle image
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)


        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            #remove the vehicle once it goes off screen
            if vehicle.rect.top >= height:
                vehicle.kill()

                #add to score
                score += 1

                # add speed to the game after passing 5 vehicles
                if score > 0 and score % 5 == 0:
                    speed += 1

        #draw the vehicles on screen
        vehicle_group.draw(screen)

        #display the score
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text_surf = font.render('Score: '+ str(score), True, white)
        text_rect = text_surf.get_rect()
        text_rect.center = (50, 450)
        screen.blit(text_surf, text_rect)

        #check if there's a head on collision
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

        #display game over screen
        if gameover:
            screen.blit(crash, crash_rect)

            pygame.draw.rect(screen, black, (0,50, width, 100))

            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)

        pygame.display.update()

        #check if the playaer wants to play again
        while gameover:
            clock.tick(fps)
            for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        gameover = False
                        running = False

                    #check for player input
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            #reset the game
                            gameover = False
                            speed = 2
                            score = 0
                            vehicle_group.empty()
                            player.rect.center = [player_x, player_y]
                        elif event.key == pygame.K_n:
                            #exit the loop
                            gameover = False
                            game_active = False
                            score = 0
                            speed = 2
                            #running = False
    # elif multiplayer_active: multiplayer
    #     # multiplayer()
    else:
        animationMenu()
        screen.fill((128, 0, 0))
        screen.blit(main_text, main_text_rect)
        screen.blit(space_text, space_text_rect)
        player.rect.center = [player_x, player_y]

    pygame.display.update()

pygame.quit()
