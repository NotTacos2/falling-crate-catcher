import pygame
import random
import os
import sys

pygame.init()

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Falling Crate Catcher")

player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))
player = pygame.image.load(os.path.join(BASE_DIR, "imgs", "cat.png")).convert_alpha()
player = pygame.transform.scale(player, (100, 100))

score = 0
highscore = 0
didwegetanewhighscore = False

if os.path.exists("savefile.txt"):
    with open("savefile.txt", "r") as file:
        highscore = int(file.read())

font = pygame.font.SysFont(None, 48)
fontonscreen = font.render("Score: " + str(score), True, (0, 0, 0)) # python really no like me if I no put str on a number
gameoverscreen = font.render("Game over. Press R to try again", True, (0, 0, 0))

falling_object = pygame.surface.Surface((50, 50))
falling_object.fill((0, 0, 0))
falling_object = pygame.image.load(os.path.join(BASE_DIR, "imgs", "crate.png")).convert_alpha()
falling_object = pygame.transform.scale(falling_object, (100, 100))

player_x = 0
player_y = 500
player_vel_x = 0
player_vel_y = 0
falling_object_x = 0
falling_object_y = 0
falling_object_vel_x = 0
falling_object_vel_y = 0.03

game_state = 1

def collision_detection():
    return (player_x <= (falling_object_x + int(falling_object.width)) and
            (player_x + player.width) >= falling_object_x and
            player_y <= (falling_object_y + falling_object.height + 5) and
            (player_y + player.height) >= falling_object_y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_state == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    player_x = 0
                    player_y = 500
                    player_vel_x = 0
                    player_vel_y = 0
                    falling_object_x = 0
                    falling_object_y = 0
                    falling_object_vel_x = 0
                    falling_object_vel_y = 0.03
                    game_state = 1
                    didwegetanewhighscore = False
                    fontonscreen = font.render("Score: " + str(score), True, (0, 0, 0))
                    window.blit(fontonscreen, (50, 50))
                    print("Restarting..")

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_vel_x = -0.2
        if event.key == pygame.K_RIGHT:
            player_vel_x = 0.2

    else:
        player_vel_x = 0
        player_vel_y = 0

    window.fill((255, 255, 255))

    if (player_x < -21.2): ## prevents players from exiting out of window's vision, I could've used windows function for this, but it's kinda confusing so um yea
        player_x = -17.8
    if (player_x > 726):
        player_x = 725.6

    if falling_object_y >= 600:
        game_state = 2

    if game_state == 1:
        player_x += player_vel_x
        player_y += player_vel_y
        falling_object_x += falling_object_vel_x
        falling_object_y += falling_object_vel_y
        window.blit(player, (player_x, player_y))
        window.blit(falling_object, (falling_object_x, falling_object_y))
        window.blit(fontonscreen, (50, 50))

        if collision_detection():
            falling_object_y = 0
            falling_object_x = random.randint(0, window.width - 50)
            score += 1
            fontonscreen = font.render("Score: " + str(score), True, (0, 0, 0)) # very scuffed fahhh
            if (falling_object_vel_y <= 0.21):
                falling_object_vel_y += 0.001
                print(falling_object_vel_y)
            window.blit(fontonscreen, (50, 50))

        if falling_object_y >= 600:
            player_x, player_y = 1000, 1000
            player_vel_x, player_vel_y = 0, 0

            falling_object_x, falling_object_y = 1000, 1000
            falling_object_vel_x, falling_object_vel_y = 0, 0

            game_state = 2

    elif game_state == 2:
        if score > highscore:
            highscore = score
            with open("savefile.txt", "w") as file:
                file.write(str(highscore))
            didwegetanewhighscore = True

        if (didwegetanewhighscore == True):
            goodjob = font.render("You went past your previous high score!", True, (0, 0, 0))
            window.blit(goodjob, (50, 150))
            
        fontonscreen = font.render("High score: " + str(highscore), True, (0, 0, 0)) # very scuffed fahhh
        window.blit(fontonscreen, (50, 100))
        window.blit(gameoverscreen, (50, 50))

    pygame.display.flip()