import pygame
import random
import sys

pygame.init()

# Константы и параметры экрана
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
font = pygame.font.SysFont(None, 35)

# Начальное состояние змейки, направление движения и позиция еды
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = (CELL_SIZE, 0)
food_pos = (300, 300)

score = 0
level = 1
speed = 10

# Функция для генерации еды в случайной позиции
def generate_food():
    while True:
        pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
               random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        if pos not in snake:
            return pos

# Функция для отображения текста на экране
def draw_text(text, pos, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, pos)

clock = pygame.time.Clock()
running = True
food_pos = generate_food()  # Генерация первой еды

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # управления
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)
    elif keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)

    # Движение змейки: добавление новой головы
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake.insert(0, head)

    # Проверка столкновений с границами или с самой собой
    if head in snake[1:] or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
        print(f'Game Over! Final Score: {score}, Level: {level}')
        pygame.quit()
        sys.exit()

    if head == food_pos:
        score += 1
        food_pos = generate_food()
        if score % 4 == 0:  # Повышение уровня каждые 4 съеденных еды
            level += 1
            speed = int(speed * 1.1)
    else:
        snake.pop()  # Удаление последнего сегмента, если еда не была съедена

    screen.fill(BLACK)
    # Отрисовка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*food_pos, CELL_SIZE, CELL_SIZE))

    # Отображение счёта и уровня
    draw_text(f'Score: {score}', (10, 10))
    draw_text(f'Level: {level}', (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
