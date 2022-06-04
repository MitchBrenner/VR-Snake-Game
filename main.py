import cv2
import pygame
import cvzone
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from snake import Snake
from food import Food

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


# Initialize pygame
pygame.init()

# Create pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# start webcam
cap = cv.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

# detection with detection confidence of 0.8 instead of .5
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Game over function
game_over_font = pygame.font.Font('Videopac-AlWA.ttf', 72)
press_key_font = pygame.font.Font('Videopac-AlWA.ttf', 24)


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,  255, 255))
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
    screen.blit(game_over_text, text_rect)

    press_key_text = press_key_font.render("Press any key to continue", True, (220, 220, 220))
    text_rect2 = press_key_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
    screen.blit(press_key_text, text_rect2)


# Score font
score = 0
score_font = pygame.font.Font('Videopac-AlWA.ttf', 32)


def score_print():
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


# Snake
snake = Snake()

# Food
food = Food(screen)

running = True
while running:

    game_over()

    # Screen background
    screen.fill((0, 0, 0))
    score_print()

    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key != pygame.K_KP_9:
                snake.alive = True
                score = 0


    if snake.alive:
        # Check to see if snake ate food
        snake_x, snake_y = snake.curr_head
        if food.x - snake.thickness < snake_x < food.x + snake.thickness \
                and food.y - snake.thickness < snake_y < food.y + snake.thickness:
            print("yum")
            score += 1
            snake.max_length += 50
            food = Food(screen)
            snake.thickness += 2

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
    else:
        game_over()


    # Screen Update
    pygame.display.update()
