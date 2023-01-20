import pygame
from utils import scale_image
pygame.font.init()

tank_factor = 0.5
bullet_factor = 0.75
terrain_factor = 1.3
button_factor = 0.4
sample_factor = 0.4

BLUE_TANK = scale_image(pygame.image.load(
    'D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\blue-tank.png'), tank_factor)
BROWN_TANK = scale_image(pygame.image.load(
    'D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\brown-tank.png'), tank_factor)
RED_TANK = scale_image(pygame.image.load(
    'D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\red-tank.png'), tank_factor)
GREEN_TANK = scale_image(pygame.image.load(
    'D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\green-tank.png'), tank_factor)

MAP1 = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map1.png'), terrain_factor)
#MAP2 = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map2.png'), terrain_factor)
#MAP3 = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map3.png'), terrain_factor)

MAP1_SAMPLE = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map1-sample.jpg'), sample_factor)
# MAP2_SAMPLE = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map2-sample.png'), sample_factor)
# MAP3_SAMPLE = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\map3-sample.png'), sample_factor)

BULLET = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\bullet.png'), bullet_factor)
WOOD_BOX = pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\wood-box.png')
STRONG_WOOD_BOX = pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\strong-wood-box.png')
HEALTH_BAR = pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\health-bar.png')
PLAY = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\play-button.png'), button_factor)
QUIT = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\quit-button.png'), button_factor)
MAIN_MENU = pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\main-menu.jpg')
SKIN = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\skin-button.png'), button_factor)

#RESUME = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\skin-button.png'), button_factor)
EXIT_TO_MENU = scale_image(pygame.image.load('D:\\Desktop\\Programmare\\pygames\\tankgame\\imgs\\quit-menu.png'), button_factor)

TITLE_FONT = pygame.font.Font('D:\\Desktop\\Programmare\\pygames\\tankgame\\fonts\\Montserrat-Bold.ttf', 120)
