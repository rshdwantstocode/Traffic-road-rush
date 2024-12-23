import os

import pygame
import random
import sys
from multiplayerClass import multiplayer

pygame.init()
#initialise the joystick module
pygame.joystick.init()
joystick_one = pygame.joystick.Joystick(0)
joystick_two = pygame.joystick.Joystick(1)

# Initialize Pygame mixer
pygame.mixer.init()

# List of audio files
audio_files = ['../musics/Deja-Vu.mp3', '../musics/Running-in-The-90s.mp3', '../musics/Gas-Gas-Gas.mp3']

# Randomly select one audio file
selected_audio = random.choice(audio_files)

# Load and play the selected audio file
pygame.mixer.music.load(selected_audio)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

#sound effect crash


# 800x480 5 inch rpi screen
width = 800
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Traffic Road Rush')

# game color
green = (1, 50, 30)
gray = (128, 128, 128)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0, 0)

alpha_value = 0  # Starting transparency (0 = fully transparent)
fade_in = True


def load_high_score(file_name="highscore.txt"):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return int(file.read())
    else:
        return 0  # If the file doesn't exist, start with a high score of 0


def save_high_score(new_high_score, file_name="highscore.txt"):
    with open(file_name, "w") as file:
        file.write(str(new_high_score))

def singlePlayer():

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
        def __init__(self, image, x, y, vehicle_scale = 1.3):
            pygame.sprite.Sprite.__init__(self)

            #scale the image so it fits in the lane
            image_scale = (50 / image.get_rect().width) * vehicle_scale
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))

            self.rect = self.image.get_rect()
            self.rect.center = [x,y]


    class PlayerVehicle(Vehicle):
        def __init__(self, x, y):
            self.image = pygame.image.load('../cars/AE86.png')
            super().__init__(self.image, x, y)



    #text in main menu
    game_font = '../font/Pixeltype.ttf'
    title_font = pygame.font.Font(game_font, 60)
    space_font = pygame.font.Font(game_font, 40)

    main_text = title_font.render('Traffic Road Rush', False, white)
    main_text_rect = main_text.get_rect(center=(400, 100))



    # Menu options
    menu_options = ["Single Player", "Multiplayer", "Quit"]
    selected_option = 0  # Index for the current selection
    cooldown = 0
    icon = pygame.image.load('../cars/burning-wheel.png')
    icon = pygame.transform.scale(icon, (50, 50))

    background_one = pygame.image.load('../cars/background1.png')
    background_one = pygame.transform.scale(background_one, (400, 200))
    # background_two = pygame.image.load('../cars/background2.png')
    # background_two = pygame.transform.scale(background_two, (400, 200))

    def draw_menu():
        screen.fill((2, 21, 38))  # Fill background
        screen.blit(background_one, (-80, 300))
        # screen.blit(background_two, (500, 300))

        screen.blit(main_text, main_text_rect)
        for idx, option in enumerate(menu_options):
            label = title_font.render(option, True, (110, 172, 218) if idx == selected_option else (255, 255, 255))
            screen.blit(label, (250, 200 + idx * 60))

            # Display the icon next to the selected option
            if idx == selected_option:
                screen.blit(icon, (200, 190 + idx * 60))

        pygame.display.flip()


    # Player's starting coordinates
    player_x = 400
    player_y = 430

    # create the player's car
    player = PlayerVehicle(player_x, player_y)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    #load the vehicles
    image_filenames = ['car1.png', 'car3.png', 'car5.png', 'car6.png', 'car7.png']
    vehicle_images = []
    for image_filename in image_filenames:
        image = pygame.image.load('../cars/'+ image_filename)
        if image_filename == 'bus.png':
            image = pygame.transform.scale(image, (150, 400))
        vehicle_images.append(image)

    #sprite group for vehicles
    vehicle_group = pygame.sprite.Group()



    # crash image
    crash = pygame.image.load('../utils/crash.png')
    crash_width, crash_height = crash.get_rect().size
    new_crash_width = int(crash_width * 0.7)  # Reduce the size by 50%
    new_crash_height = int(crash_height * 0.7)

    crash = pygame.transform.scale(crash, (new_crash_width, new_crash_height))
    crash_rect = crash.get_rect()


    # game settings
    gameover = False
    speed = 4
    score = 0
    high_score = load_high_score()

    # game loop
    clock = pygame.time.Clock()
    fps = 60
    game_active = False
    multiplayer_active = False
    running = True
    spawn_rate = 120  # Initial delay between spawns in frames (higher = slower)

    #controllers
    joysticks = {}


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

            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")
            #
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        for joystick in joysticks.values():

            horizontal_move = joystick_one.get_axis(0)
            player.rect.x += horizontal_move * 5
            vertical_move = joystick_one.get_axis(1)
            player.rect.y += vertical_move * 5

            # Ensure the player stays within the road boundaries
            if player.rect.left < 200:  # Left road boundary
                player.rect.left = 200
            elif player.rect.right > 595:  # Right road boundary
                player.rect.right = 595

            if player.rect.top < 0:
                player.rect.top = 0
            elif player.rect.bottom > height:
                player.rect.bottom = height



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

            # #add up to two vehicles
            if len(vehicle_group) < 5:

                #ensure there's enough gap between vehicles
                add_vehicle = True
                for vehicle in vehicle_group:
                    if vehicle.rect.top < vehicle.rect.height:
                        add_vehicle = False

                vehicle_spawn_scale = 1.5
                if add_vehicle:
                    #select a random lane
                    lane = random.choice((263, 405, 540))

                    #select a random vehicle image
                    image = random.choice(vehicle_images)
                    vehicle = Vehicle(image, lane, height / -2, vehicle_scale = vehicle_spawn_scale)
                    vehicle_group.add(vehicle)

            if score > high_score:
                high_score = score  # Update the high score
                save_high_score(high_score)  # Save the new high score to the file

                # Display the high score on screen (optional)
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            high_score_text = font.render('High Score: ' + str(high_score), False, white)
            high_score_rect = high_score_text.get_rect(center=(700, 50))
            screen.blit(high_score_text, high_score_rect)




            for vehicle in vehicle_group:
                vehicle.rect.y += speed
                #remove the vehicle once it goes off screen
                if vehicle.rect.top >= height:
                    vehicle.kill()

                    #add to score
                    score += 1

                   # add speed to the game after passing 5 vehicles
                    if score > 0 and score % 5 == 0:
                        speed += 0.7

            #draw the vehicles on screen
            vehicle_group.draw(screen)

            #display the score
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text_surf = font.render('Score: '+ str(score), False, white)
            text_rect = text_surf.get_rect()
            text_rect.center = (50, 50)
            screen.blit(text_surf, text_rect)

            #check if there's a head on collision
            if pygame.sprite.spritecollide(player, vehicle_group, True):
                gameover = True
                crash_rect.center = [player.rect.center[0], player.rect.top]

            #display game over screen
            if gameover:
                pygame.mixer.music.load('../sound/crash.mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(loops=1)
                screen.blit(crash, crash_rect)

                pygame.draw.rect(screen, black, (0,43, width, 250))

                font = pygame.font.Font(pygame.font.get_default_font(), 16)
                text = font.render('Game over. Play again? Enter A to play again, B to quit', False, white)
                text_rect = text.get_rect(center=(width / 2, 100))

                high_score_text = font.render('High Score: ' + str(high_score), False, white)
                high_score_rect = high_score_text.get_rect(center=(width / 2, 150))

                score_text = font.render('Score: ' + str(score), False, white)
                score_text_rect = score_text.get_rect(center=(width / 2, 230))

                if score >= high_score:
                    new_high_score = font.render('NEW HIGH SCORE!!', False, yellow)
                    new_high_score_rect = new_high_score.get_rect(center=(width / 2, 200))
                    screen.blit(new_high_score, new_high_score_rect)

                screen.blit(score_text, score_text_rect)
                screen.blit(high_score_text, high_score_rect)
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
                                speed = 4
                                score = 0
                                vehicle_group.empty()
                                player.rect.center = [player_x, player_y]
                            elif event.key == pygame.K_n:
                                #exit the loop
                                gameover = False
                                game_active = False
                                score = 0
                                speed = 4
                                vehicle_group.empty()
                                player.rect.center = [player_x, player_y]
                                #running = False
                for joystick in joysticks.values():
                    #exit the game
                    if joystick_one.get_button(8):
                        print("game over exit")

                    if joystick_one.get_button(1):
                        # reset the game
                        gameover = False
                        speed = 4
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif joystick_one.get_button(0):
                        # exit the loop
                        gameover = False
                        game_active = False
                        score = 0
                        speed = 4
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                        # running = False

        elif multiplayer_active: #multiplayer
            # print(multiplayer_active
            multiplayer(0, 0)
            multiplayer_active = False
        else:
            draw_menu()

            # Get vertical axis movement (axis 1)
            vertical_move = joystick_one.get_axis(1)

            # Cooldown to prevent rapid selection change
            if cooldown == 0:
                if vertical_move > 0.5:  # Down movement
                    selected_option = (selected_option + 1) % len(menu_options)
                    cooldown = 15  # Set cooldown for smoother navigation
                elif vertical_move < -0.5:  # Up movement
                    selected_option = (selected_option - 1) % len(menu_options)
                    cooldown = 15

            # Execute action if button is pressed (e.g., button 9 to select)
            if joystick_one.get_button(1):
                if selected_option == 0:  # Single Player
                    game_active = True
                elif selected_option == 1:  # Multiplayer
                    print("Starting Multiplayer...")
                    multiplayer_active = True
                elif selected_option == 2:  # Quit
                    pygame.quit()
                    sys.exit()

            # Cooldown countdown
        if cooldown > 0:
            cooldown -= 1

            player.rect.center = [player_x, player_y]

        pygame.display.update()

    pygame.quit()


singlePlayer()