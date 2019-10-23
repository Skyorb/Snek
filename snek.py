#!/usr/bin/env python3
from typing import List, Tuple, Deque

import pygame
from pygame import Surface
from pygame.time import Clock
from collections import deque
from random import choice, randint

SIZE = WIDTH, HEIGHT = 800, 600
BLACK = pygame.Color(0x000000FF)
WHITE = pygame.Color(0xFFFFFFFF)

TARGET_SIZE = 10

FPS = 120

# Richtungsangaben

LEFT = -1, 0
RIGHT = 1, 0
UP = 0, -1
DOWN = 0, 1


def move(head: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    current_x, current_y = head
    modifier_x, modifier_y = direction
    return current_x + modifier_x, current_y + modifier_y


def point_is_in_rect(point: Tuple[int, int], rect: Tuple[int, int, int, int]) -> bool:
    px, py = point
    rx, ry, rw, rh = rect
    return rx <= px < (rx + rw) and ry <= py < (ry + rh)


def generate_target(snake: Deque[Tuple[int, int]]) -> Tuple[int, int, int, int]:  # rect mit x, y, width, height
    collision: bool = True
    while collision:
        target = randint(11, 790 - TARGET_SIZE), randint(51, 500 - TARGET_SIZE), TARGET_SIZE, TARGET_SIZE
        collision = False
        for point in snake:
            if point_is_in_rect(point, target):
                collision = True
    return target


def main():
    pygame.init()
    screen: Surface = pygame.display.set_mode(SIZE)
    clock = Clock()

    direction = choice([UP, DOWN, LEFT, RIGHT])  # Startet in irgendeine Richtung
    snake: Deque[Tuple[int, int]] = deque([(randint(100, WIDTH - 100), randint(100, HEIGHT - 100))],
                                          maxlen=100)  # Deque importieren, Random INT Startposition
    target = generate_target(snake)

    running: bool = True
    while running:
        switched_direction = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not switched_direction:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                    switched_direction = True
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                    switched_direction = True
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                    switched_direction = True
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                    switched_direction = True

        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, (10, 50, WIDTH - 20, HEIGHT - 60), 1)
        pygame.draw.rect(screen, WHITE, target)

        for point in snake:
            screen.set_at(point, WHITE)

        pygame.display.flip()

        new_head = move(snake[-1], direction)
        if screen.get_at(new_head) == WHITE:
            if point_is_in_rect(new_head, target):
                target = generate_target(snake)
                snake = deque(snake, maxlen=snake.maxlen +25)
            else:
                running = False
        snake.append(new_head)

        clock.tick(FPS)

    pygame.quit()
    print(f' Game Over! Your Score: {len(snake)}')


if __name__ == '__main__':
    main()
