import math
import random
import pygame


class Snake:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.current_length = 0  # total length of the snake
        self.max_length = 150  # total allowed length
        self.previous_head = 0, 0  # previous head point
        self.curr_head = 0, 0
        self.thickness = 10

    def update(self, screen, curr_x, curr_y):

        # set snake head
        self.curr_head = curr_x, curr_y

        r, g, b = random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)

        pygame.draw.circle(screen, (r, g, b), (curr_x, curr_y), self.thickness // 2)

        # if self.points:
        #     end_points = self.points[0]
        #     pygame.draw.circle(screen, (r, g, b), end_points, self.thickness // 2)

        prev_x, prev_y = self.previous_head

        self.points.append((curr_x, curr_y))

        distance = math.hypot(curr_x - prev_x, curr_y - prev_y)
        self.lengths.append(distance)
        self.current_length += distance
        self.previous_head = curr_x, curr_y

        # length reduction
        if self.current_length > self.max_length:
            for i, length in enumerate(self.lengths):
                self.current_length -= length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.current_length < self.max_length:
                    break

        for i, point in enumerate(self.points):
            if i != 0:
                pygame.draw.line(screen, (r, g, b), self.points[i - 1], self.points[i], self.thickness)
