import math
import random
import pygame
from scipy import interpolate
import numpy as np
import cv2 as cv


class Snake:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.current_length = 0  # total length of the snake
        self.max_length = 150  # total allowed length
        self.previous_head = 0, 0  # previous head point
        self.curr_head = 0, 0
        self.thickness = 10
        self.smooth_points = []
        self.alive = True

    @staticmethod
    def b_spline(waypoints):
        x = []
        y = []
        smooth = []

        for points in waypoints:
            x.append(points[0])
            y.append(points[1])

        if x:
            tck, *rest = interpolate.splprep((x, y), k=1)
            u = np.linspace(0, 1, num=50)
            smooth = interpolate.splev(u, tck)

        return smooth

    def collision_check(self, head_point, screen):
        curr_x, curr_y = head_point
        min_distance = 100

        for point in self.points[:-5]:
            x, y = point
            min_distance = math.sqrt(math.pow(x - curr_x, 2) + math.pow(y - curr_y, 2))

        # points = np.array(self.points[:-10], np.int64)  # take all points but the last two
        # points = points.reshape((-1, 1, 2))
        # min_distance = cv.pointPolygonTest(points, head_point, True)  # true to return measure distance
            if -10 < min_distance < 10:
                print("hit")
                self.alive = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.current_length = 0  # total length of the snake
                self.max_length = 150  # total allowed length
                self.previous_head = 0, 0  # previous head point
                self.thickness = 10
                self.alive = False



    def update(self, screen, curr_x, curr_y):

        # set snake head
        self.curr_head = curr_x, curr_y

        r, g, b = random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)

        pygame.draw.circle(screen, (r, g, b), (curr_x, curr_y), self.thickness // 2)

        # if self.points:
        #     end_points = self.points[0]
        #     pygame.draw.circle(screen, (r, g, b), end_points, self.thickness // 2)

        self.collision_check((curr_x, curr_y), screen)

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

        if len(self.points) > 1:
            try:
                self.smooth_points = self.b_spline(self.points)

                x, y = self.smooth_points

                for x, y in zip(x, y):
                    pygame.draw.circle(screen, (r, g, b), (x, y), self.thickness // 2, 0)
            except:
                pass


        # for i, point in enumerate(self.smooth_points):
        #     if i > 1:
        #
        #         pygame.draw.line(screen, (r, g, b), self.smooth_points[i - 1], self.smooth_points[i], 100)
        #         # cv.line(screen, self.points[i - 1], self.points[i], (r,g,b), self.thickness)
