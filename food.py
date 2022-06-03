import random

import pygame.draw


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = random.randint(100, 1100), random.randint(100, 700)
        self.r, self.g, self.b = random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)

    def update(self):
        pygame.draw.circle(self.screen, (self.r, self.g, self.b), (self.x, self.y), 10)
