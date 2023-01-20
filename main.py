'''
TO DO:
    -De rezolvat problema cu textul(de printat pe unde si cum treb)
    -De implementat texturile lu darius(daca sunt, sper sa fie)
    -De implementat pana la capat alegerea mapei
    -De implementat tinerea minte a skinurilor
    -De implementat interfata mai avansata a meniului cu skinuri(de aratat skinurile selectate)
    -Cam asa, daca mai este ceva, de implementat, de facut ultimele poleiri
'''


import pygame
import math
import random
from utils import blit_rotate_center, scale_image, rotate_pivot_point
from classes import PlayerTank, Bullet, Particle
from funcs import (recting_obstacles, bullet_handle, collision_handling,
    input_handling, draw_game, draw_main_menu, draw_misc_menu, choose_skin,
    winning, draw_ingame_menu, draw_ingame_menu_mask, draw_health_bar, particle_handle)
from sprites_init import (BLUE_TANK, BROWN_TANK, RED_TANK, GREEN_TANK, MAP1,
    MAP1_SAMPLE, BULLET, WOOD_BOX, PLAY, QUIT, MAIN_MENU, SKIN, EXIT_TO_MENU,
    TITLE_FONT, STRONG_WOOD_BOX, HEALTH_BAR)

pygame.font.init()

#Window setup
WIDTH, HEIGHT = MAIN_MENU.get_width(), MAIN_MENU.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tank Game')

#Loop variables
FPS = 60
clock = pygame.time.Clock()

run_game = True
run_menu = True
run_map = True
run_skin = True
run_ingame_pause = True

click_menu = False
click_map = False
click_skin = False
click_ingame_pause = False

default1_skin = BLUE_TANK
default2_skin = BROWN_TANK

TITLE_GREEN = (34,139,34)
ROUNDS = 5
player1_wins = 0
player2_wins = 0
ticks_hit = 10

health_surf_out1 = pygame.Surface((72, 9))
health_surf_out2 = pygame.Surface((72, 9))

#Player instances
player1 = PlayerTank(3, 3, default1_skin, (150, 350))
player2 = PlayerTank(3, 3, default2_skin, (550, 350))

#Buttons/Rects
play_button = PLAY.get_rect(topleft=((WIDTH/2 - PLAY.get_width())/2 + 10, 370))
skin_button = SKIN.get_rect(topleft=(3*WIDTH/4 - SKIN.get_width()/2 - 10, 370))
quit_button = QUIT.get_rect(topleft=((WIDTH - QUIT.get_width())/2, 520))

exit_to_menu = EXIT_TO_MENU.get_rect(topleft=(325, 520))
map1_but = MAP1_SAMPLE.get_rect(topleft=(130, 200))
# map2_but = MAP2_SAMPLE.get_rect(topleft=(300, 500))
# map3_but = MAP3_SAMPLE.get_rect(topleft=(300, 700))

p1_skin_option1 = BROWN_TANK.get_rect(topleft=(150, 200))
p1_skin_option2 = BLUE_TANK.get_rect(topleft=(150, 400))
p1_skin_option3 = RED_TANK.get_rect(topleft=(300, 200))
p1_skin_option4 = GREEN_TANK.get_rect(topleft=(300, 400))
p2_skin_option1 = BROWN_TANK.get_rect(topleft=(600, 200))
p2_skin_option2 = BLUE_TANK.get_rect(topleft=(600, 400))
p2_skin_option3 = RED_TANK.get_rect(topleft=(900, 200))
p2_skin_option4 = GREEN_TANK.get_rect(topleft=(900, 400))

#Text
some_text = TITLE_FONT.render('Tankgame', True, TITLE_GREEN)

#Main variables
images_menu = [(MAIN_MENU, (0, 0)) ,(PLAY, play_button.topleft), (SKIN, skin_button.topleft), (QUIT, quit_button.topleft),
    (some_text, (WIDTH/2 - some_text.get_width()/2, 50))]

images_game = [(MAP1, (0,0))]

images_map_options = [(MAIN_MENU, (0, 0)), (MAP1_SAMPLE, map1_but.topleft)]

images_skin_options = [(MAIN_MENU, (0, 0)), (BROWN_TANK, p1_skin_option1.topleft), (BROWN_TANK, p2_skin_option1.topleft),
    (BLUE_TANK, p1_skin_option2.topleft), (BLUE_TANK, p2_skin_option2.topleft),
    (RED_TANK, p1_skin_option3.topleft), (RED_TANK, p2_skin_option3.topleft),
    (GREEN_TANK, p1_skin_option4.topleft), (GREEN_TANK, p2_skin_option4.topleft)]

images_ingame_pause = []

winner = None
bullets_cap = 40
bullets1 = []
bullets2 = []
particles1 = []
particles2 = []
particles1_hit = []
particles2_hit = []
obstacles = [(WOOD_BOX, (400, 400)), (STRONG_WOOD_BOX, (200, 150))]
obstacles_rect = []
recting_obstacles(obstacles, obstacles_rect)

#Main loops
def main_menu(run_menu, click_menu):
    while run_menu:
        clock.tick(FPS)

        draw_main_menu(WIN, images_menu)

        mx, my = pygame.mouse.get_pos()
        if play_button.collidepoint((mx, my)):
            if click_menu:
                map_options(run_map, run_game, click_map)
                run_menu = False
                break
        if skin_button.collidepoint((mx, my)):
            if click_menu:
                skin_options(run_skin, click_skin, player1, player2)
                run_menu = False
                break
        if quit_button.collidepoint((mx, my)):
            if click_menu:
                run_menu = False
                break

        click_menu = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                break
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_menu = False
                    break
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_menu = True

def skin_options(run_skin, click_skin, player1, player2):
    while run_skin:
        clock.tick(FPS)

        draw_misc_menu(WIN, images_skin_options)
        choose_skin(tanks, player_skin_options, player1, player2, click_skin)

        click_skin = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_skin = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(run_menu, click_menu)
                    run_skin = False
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_skin = True

def map_options(run_map, run_game, click_map):
    while run_map:
        clock.tick(FPS)

        draw_misc_menu(WIN, images_map_options)

        mx, my = pygame.mouse.get_pos()
        if map1_but.collidepoint((mx, my)):
            if click_map:
                game(run_game)
                run_map = False
                break

        click_map = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_map = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(run_menu, click_menu)
                    run_map = False
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_map = True

def game(run_game):
    while run_game:
        clock.tick(FPS)

        draw_game(WIN, images_game, player1, player2, obstacles, bullets1, bullets2, particles1, particles2, particles1_hit, particles2_hit, HEALTH_BAR, health_surf_out1, health_surf_out2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    bullet_handle(player1, player2, True, False, bullets_cap, bullets1, bullets2, BULLET, WIN)
                if event.key == pygame.K_RSHIFT:
                    bullet_handle(player1, player2, False, True, bullets_cap, bullets1, bullets2, BULLET, WIN)
                if event.key == pygame.K_ESCAPE:
                    pause_menu(run_ingame_pause, images_ingame_pause, click_ingame_pause)
                    run_game = False
                    break

        for bullet in bullets1:
            bullet.move()
        for bullet in bullets2:
            bullet.move()

        collision_handling(player1, player2, bullets1, bullets2, obstacles_rect, WIDTH, HEIGHT, ticks_hit, WIN, particles1_hit, particles2_hit)
        input_handling(player1, player2, WIN, particles1, particles2)
        particle_handle(player1, particles1, particles1_hit)
        particle_handle(player2, particles2, particles2_hit)

        winning(player1, player2, player1_wins, player2_wins, ROUNDS, winner)

def pause_menu(run_ingame_pause, images_ingame_pause, click_ingame_pause):
    draw_ingame_menu_mask(WIN)

    while run_ingame_pause:
        clock.tick(FPS)

        draw_ingame_menu(WIN, images_ingame_pause)

        mx, my = pygame.mouse.get_pos()
        if map1_but.collidepoint((mx, my)):
            if click_ingame_pause:
                game(run_game)
                run_ingame_pause = False
                break

        click_ingame_pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_ingame_pause = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game(run_game)
                    run_ingame_pause = False
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_ingame_pause = True

main_menu(run_menu, click_menu)
pygame.quit()
