import cv2
import pygame
import cvzone
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from snake import Snake
from food import Food

# Initialize pygame
pygame.init()

# Create pygame screen
screen = pygame.display.set_mode((1200, 800))

# start webcam
cap = cv.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

# detection with detection confidence of 0.8 instead of .5
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Snake
snake = Snake()

# Food
food = Food(screen)

running = True
while running:

    # Screen background
    screen.fill((255, 255, 255))

    # Check to see if snake ate food
    snake_x, snake_y = snake.curr_head
    if food.x - snake.thickness < snake_x < food.x + snake.thickness \
            and food.y - snake.thickness < snake_y < food.y + snake.thickness :
        print("yum")
        snake.max_length += 50
        food = Food(screen)
        snake.thickness += 2

    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Reading points from opencv
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    # hands is a dictionary with access to points
    if hands:
        landmark_list = hands[0]['lmList']
        # element at 8 will give us xyz, and we do not need z so just get x, y by using range
        pointIndex = landmark_list[8][0:2]

        head_x, head_y = pointIndex
        snake.update(screen, head_x, head_y)

    # Add food
    food.update()

    # Screen Update
    pygame.display.update()

