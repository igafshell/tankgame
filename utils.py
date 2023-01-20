import pygame
import math

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image =  pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def rotate_pivot_point(player, px, py, angle):
    cx, cy = player.img.get_rect(topleft=(player.x, player.y)).center

    player_angle_radians = math.radians(-angle)
    c = math.cos(player_angle_radians)
    s = math.sin(player_angle_radians)

    rotated_x = cx + c * (px - cx) - s * (py - cy)
    rotated_y = cy + s * (px - cx) + c * (py - cy)

    return (rotated_x, rotated_y)
