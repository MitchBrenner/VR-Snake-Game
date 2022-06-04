import random

import pygame.draw


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = random.randint(200, 1000), random.randint(200, 600)
        self.r, self.g, self.b = random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)

    def update(self):
        pygame.draw.circle(self.screen, (self.r, self.g, self.b), (self.x, self.y), 10)
