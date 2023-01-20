import pygame
import math
from utils import blit_rotate_center, scale_image
import random

class PlayerTank:

    def __init__(self, max_vel, rotation_vel, img, start_pos):
        self.img = img
        self.rotation_vel = rotation_vel
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 0
        self.start_pos = start_pos
        self.x, self.y = self.start_pos
        self.acceleration = 0.1
        self.health = 100

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
            if self.angle > 360:
                self.angle = 0
        elif right:
            self.angle -= self.rotation_vel
            if self.angle < 0:
                self.angle = 360

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def collide(self, mask, x=0, y=0):
        tank_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(tank_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0
        self.health = 100

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -0.7 * self.vel
        self.move()

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


class Bullet:
    def __init__(self, vel, pos, angle, img):

        self.angle = angle
        self.vel1 = vel
        self.vel2 = vel
        self.img = img
        self.x, self.y = pos

    def move(self, ver_neg=False, hoz_neg=False):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel2
        horizontal = math.sin(radians) * self.vel1
        if ver_neg:
            self.vel2 *= -1
        if hoz_neg:
            self.vel1 *= -1
        self.x -= horizontal
        self.y -= vertical

    def collide(self, mask, x=0, y=0):
        tank_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(tank_mask, offset)
        return poi

    def reflect(self, obstacle_rect, bullet_rect):
        collisison_tollerance = 50

        if bullet_rect.colliderect(obstacle_rect):
            if abs(obstacle_rect.top - bullet_rect.bottom) < collisison_tollerance:
                self.vel2 *= -1
            if abs(obstacle_rect.bottom - bullet_rect.top) < collisison_tollerance:
                self.vel2 *= -1
            if abs(obstacle_rect.left - bullet_rect.right) < collisison_tollerance:
                self.vel1 *= -1
            if abs(obstacle_rect.right - bullet_rect.left) < collisison_tollerance:
                self.vel1 *= -1

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

class Particle:
    def __init__(self, location, color, timer, radius, vel_x, vel_y):
        self.timer = timer
        self.x, self.y = location
        self.vel_x, self.vel_y = vel_x, vel_y
        self.color = color
        self.radius = self.timer * radius

    def particle_dissapear(self, particle, particles):
        particle.x += self.vel_x
        particle.y += self.vel_y
        if self.radius == 1:
            pass
        else:
            self.radius -= 0.1
        if self.timer <= 0:
            particles.remove(particle)
        self.timer -= 0.1

    def draw_particle(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class SpecParticle(Particle):
    def __init__(self, location, r, g, b, timer, radius, vel_x, vel_y):
        self.timer = timer
        self.x, self.y = location
        self.vel_x, self.vel_y = vel_x, vel_y
        self.radius = self.timer * radius
        self.r, self.g, self.b = r, g, b

    def draw_particle(self, win):
        if self.r > 44:
            self.r -= 2.5
        if self.g > 15:
            self.g -= 2.5
        pygame.draw.circle(win, (self.r, self.g, self.b), (self.x, self.y), self.radius)
