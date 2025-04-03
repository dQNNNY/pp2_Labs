import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Экран и шрифт
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
font = pygame.font.SysFont(None, 35)

# Змейка и еда
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = (CELL_SIZE, 0)

# Счёт и уровень
score = 0
level = 1
speed = 10

# Параметры еды
food_pos = (300, 300)
food_weight = 1
food_timer = 0
food_lifetime = 5000  # Время исчезновения еды (в мс)

# Генерация новой еды с разными весами и таймером
def generate_food():
    while True:
        pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
               random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        if pos not in snake:
            global food_weight, food_timer
            food_weight = random.choice([1, 2, 3])
            food_timer = pygame.time.get_ticks()
            return pos

# Функция для отображения текста
def draw_text(text, pos, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, pos)

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
food_pos = generate_food()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)
    elif keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)

    # Движение змейки
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake.insert(0, head)

    # Проверка на столкновение с границей или с собой
    if head in snake[1:] or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
        print(f'Game Over! Final Score: {score}, Level: {level}')
        pygame.quit()
        sys.exit()

    # Проверка на поедание еды
    if head == food_pos:
        score += food_weight
        food_pos = generate_food()
        # Повышение уровня каждые 4 очка
        if score % 4 == 0:
            level += 1
            speed = int(speed * 1.1)
    else:
        snake.pop()

    # Проверка таймера для еды
    if pygame.time.get_ticks() - food_timer >= food_lifetime:
        food_pos = generate_food()

    # Отрисовка
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*food_pos, CELL_SIZE, CELL_SIZE))

    # Отображение счёта, уровня и веса еды
    draw_text(f'Score: {score}', (10, 10))
    draw_text(f'Level: {level}', (10, 40))
    draw_text(f'Food Weight: {food_weight}', (10, 70))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()