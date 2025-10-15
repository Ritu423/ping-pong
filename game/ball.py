import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, wall_sound=None):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Top/bottom wall bounce
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if wall_sound:
                wall_sound.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if wall_sound:
                wall_sound.play()

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
