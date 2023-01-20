import math
import pygame
import random
from classes import Bullet, Particle, SpecParticle
from utils import blit_rotate_center, rotate_pivot_point
from sprites_init import TITLE_FONT

def recting_obstacles(obstacles, obstacles_rect):
    for obstacle in obstacles:
        obstacle_rectified = pygame.Rect(obstacle[1], (obstacle[0].get_width(), obstacle[0].get_height()))
        obstacles_rect.append(obstacle_rectified)

def bullet_handle(player1, player2, player1_shot, player2_shot, bullets_cap, bullets1, bullets2, bullet_img, win):
    bullet_x1, bullet_y1 = player1.x + player1.img.get_width()/2 - bullet_img.get_width()/2, player1.y
    bullet_x2, bullet_y2 = player2.x + player2.img.get_width()/2 - bullet_img.get_width()/2, player2.y

    if player1_shot and not player2_shot:
        if len(bullets1) < bullets_cap:
            bullets1.append(Bullet(6, rotate_pivot_point(player1, bullet_x1, bullet_y1, player1.angle), player1.angle, bullet_img))

    if player2_shot and not player1_shot:
        if len(bullets2) < bullets_cap:
            bullets2.append(Bullet(6, rotate_pivot_point(player2, bullet_x2, bullet_y2, player2.angle), player2.angle, bullet_img))

def collision_handling(player1, player2, bullets1, bullets2, obstacles_rect, width, height, ticks_hit, win, particles1_hit, particles2_hit):
    player1_rect = player1.img.get_rect(topleft=(player1.x, player1.y))
    player2_rect = player2.img.get_rect(topleft=(player2.x, player2.y))

    #player colision handling
    if player1.x <= 0 or player1.x >= width - player1.img.get_width():
        player1.bounce()
    if player1.y <= 0 or player1.y + 5 >= height - player1.img.get_height():
        player1.bounce()

    if player2.x <= 0 or player2.x >= width - player2.img.get_width():
        player2.bounce()
    if player2.y <= 0 or player2.y + 5 >= height - player2.img.get_height():
        player2.bounce()

    for obstacle_rect in obstacles_rect:
        if player1_rect.colliderect(obstacle_rect):
            player1.bounce()
        if player2_rect.colliderect(obstacle_rect):
            player2.bounce()

    if player1_rect.colliderect(player2_rect):
        if player1.vel != 0:
            player1.bounce()
        if player2.vel != 0:
            player2.bounce()

        if ticks_hit % 10 == 0:
            player1.health -= abs(player2.vel)
            player2.health -= abs(player1.vel)
            print(f'P1 Health: {player1.health}')
            print(f'P2 Health: {player2.health}')
        ticks_hit += 1
    else:
        ticks_hit = 0

    #player1 bullets collision_handling
    for bullet in bullets1:
        if bullet.x < 0 or bullet.x >= width - bullet.img.get_width():
            if bullet in bullets1:
                bullets1.remove(bullet)
        if bullet.y < 0 or bullet.y >= height - bullet.img.get_height():
            if bullet in bullets1:
                bullets1.remove(bullet)

        #Collision with the other player
        bullet_rect =  pygame.Rect((bullet.x, bullet.y),
            (bullet.img.get_width(), bullet.img.get_height()))

        if bullet_rect.colliderect(player2_rect):
            player2.health -= 20
            print(player2.health)
            if bullet in bullets1:
                bullets1.remove(bullet)
            particles_hit(win, player2, particles1_hit)

        #Collision with obstacles
        for obstacle_rect in obstacles_rect:
            bullet.reflect(obstacle_rect, bullet_rect)

    #Player2 bullets collision_handling
    for bullet in bullets2:
        if bullet.x < 0 or bullet.x >= width - bullet.img.get_width():
            if bullet in bullets2:
                bullets2.remove(bullet)

        if bullet.y < 0 or bullet.y >= height - bullet.img.get_height():
            if bullet in bullets2:
                bullets2.remove(bullet)

        #Collision with the other player
        bullet_rect =  pygame.Rect((bullet.x, bullet.y),
            (bullet.img.get_width(), bullet.img.get_height()))

        if bullet_rect.colliderect(player1_rect):
            player1.health -= 0.1
            print(player1.health)
            if bullet in bullets2:
                bullets2.remove(bullet)
            particles_hit(win, player1, particles2_hit)

        #Collision with obstacles
        for obstacle_rect in obstacles_rect:
            bullet.reflect(obstacle_rect, bullet_rect)

def particles_hit(win, player, particles_hit):
    radius = 2.2
    for i in range(10):
        vel_x, vel_y = random.randint(0, 20) / 10 - 1, random.randint(0, 25) / 10 - 1
        px, py = player.img.get_rect(topleft=(player.x, player.y)).center
        timer = random.randint(2, 4)
        color = (255, 125, 0) #255-125 = 105, 55
        particles_hit.append(SpecParticle((px, py), 255, 120, 0, timer, radius, vel_x, vel_y))

def choose_skin(tanks, player_skin_options, player1, player2, click_skin):
    mx, my = pygame.mouse.get_pos()
    if player_skin_options[0].collidepoint((mx, my)):
        if click_skin:
            player1.img = tanks[0]
    if player_skin_options[1].collidepoint((mx, my)):
        if click_skin:
            player1.img = tanks[1]
    if player_skin_options[2].collidepoint((mx, my)):
        if click_skin:
            player1.img = tanks[2]
    if player_skin_options[3].collidepoint((mx, my)):
        if click_skin:
            player1.img = tanks[3]
    if player_skin_options[4].collidepoint((mx, my)):
        if click_skin:
            player2.img = tanks[0]
    if player_skin_options[5].collidepoint((mx, my)):
        if click_skin:
            player2.img = tanks[1]
    if player_skin_options[6].collidepoint((mx, my)):
        if click_skin:
            player2.img = tanks[2]
    if player_skin_options[7].collidepoint((mx, my)):
        if click_skin:
            player2.img = tanks[3]

def winning(player1, player2, player1_wins, player2_wins, rounds, winner):
    if player1_wins + player2_wins >= rounds:
        if player1_wins > player2_wins:
            winner = player1
            print('Player1 won this match!')
        if player1_wins < player2_wins:
            winnner = player2
            print('Player2 won this match!')
    else:
        if player1.health <= 0 and player2.health <= 0:
            print('Draw')
            player1.reset()
            player2.reset()

        elif player1.health <= 0:
            player2_wins += 1
            print('Player2 won this round!')
            player1.reset()
            player2.reset()

        elif player2.health <= 0:
            player1_wins += 1
            print('Player1 won this round')
            player1.reset()
            player2.reset()

def input_handling(player1, player2, win, particles1, particles2):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player1.rotate(left=True)
    if keys[pygame.K_d]:
        player1.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player1.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player1.move_backward()
    if not moved:
        player1.reduce_speed()

    if keys[pygame.K_LEFT]:
        player2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player2.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player2.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player2.move_backward()
    if not moved:
        player2.reduce_speed()

def particle_handle(player, particles, particles_hit):
    if abs(player.vel) - 0.3 > 0:
        px = player.x + player.img.get_width()/2 + random.randint(-5, 5)
        py = player.y + player.img.get_height() + random.randint(-5, 5)
        vel_x, vel_y = random.randint(0, 10) / 10 - 1, -0.5

        particles.append(Particle(rotate_pivot_point(player, px, py, player.angle),
            (139, 69, 19), random.randint(1, 4), 1.75, vel_x, vel_y))

    for particle in particles:
        if particle in particles:
            particle.particle_dissapear(particle, particles)
    for particle in particles_hit:
        if particle in particles_hit:
            particle.particle_dissapear(particle, particles_hit)


def draw_misc_menu(win, local_images):
    for img, pos in local_images:
        win.blit(img, pos)

    pygame.display.update()

def draw_main_menu(win, images_menu):
    for img, pos in images_menu:
        win.blit(img, pos)

    pygame.display.update()

def draw_ingame_menu_mask(win):
    opacity = 128
    mask_win = pygame.Surface((win.get_width(), win.get_height()))
    mask_win.fill((0, 0, 0))
    mask_win.set_alpha(opacity)
    win.blit(mask_win, (0, 0))

def draw_ingame_menu(win, images_ingame_pause):
    for img, pos in images_ingame_pause:
        win.blit(img, pos)

    pygame.display.update()

# test1 = pygame.Surface((15, 15))
# test2 = pygame.Surface((15, 15))

def draw_health_bar(win, player, health_bar, health_surf_out):
    health_surf_in = pygame.Surface((health_surf_out.get_width()*(player.health/100),health_surf_out.get_height()))
    health_surf_in.fill((255, 0, 0))
    health_surf_out.fill((0, 0, 0))

    win.blit(health_surf_out, (player.x - player.img.get_width()/2 + 3, player.y - 17))
    win.blit(health_surf_in, (player.x - player.img.get_width()/2 + 3, player.y - 17))
    win.blit(health_bar, (player.x - player.img.get_width()/2, player.y - 20))

def draw_game(win, images_game, player1, player2, obstacles, bullets1, bullets2, particles1, particles2, particles1_hit, particles2_hit, HEALTH_BAR, health_surf_out1, health_surf_out2):
    for img, pos in images_game:
        win.blit(img, pos)
    for img, pos in obstacles:
        win.blit(img, pos)

    player1.draw(win)
    player2.draw(win)

    draw_health_bar(win, player1, HEALTH_BAR, health_surf_out1)
    draw_health_bar(win, player2, HEALTH_BAR, health_surf_out2)

    for bullet in bullets1:
        bullet.draw(win)
    for bullet in bullets2:
        bullet.draw(win)

    for particle in particles1_hit:
        particle.draw_particle(win)
    for particle in particles2_hit:
        particle.draw_particle(win)
    for particle in particles1:
        particle.draw_particle(win)
    for particle in particles2:
        particle.draw_particle(win)

    # bullet_x1, bullet_y1 = player1.x + player1.img.get_width()/2, player1.y
    # bullet_x2, bullet_y2 = player2.x + player2.img.get_width()/2, player2.y
    # test1.fill((0, 0, 255))
    # test2.fill((0, 0, 255))
    # x1, y1 = rotate_pivot_point(player1, bullet_x1, bullet_y1)
    # x2, y2 = rotate_pivot_point(player2, bullet_x2, bullet_y2)
    # win.blit(test1, (x1-7.5, y1))
    # win.blit(test2, (x2-7.5, y2))
    pygame.display.update()
