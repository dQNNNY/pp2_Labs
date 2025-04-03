import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Paint App')
screen.fill(WHITE)

# Переменные для рисования
current_color = BLACK
brush_size = 5
shape_mode = 'brush'

# Функция для отображения цветовой палитры
def draw_color_palette():
    colors = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i*40, 10, 30, 30))

# Функция для рисования равностороннего треугольника
def draw_equilateral_triangle(start_pos, end_pos, color):
    side_length = int(math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2))
    height = int((math.sqrt(3)/2) * side_length)
    point1 = start_pos
    point2 = (start_pos[0] + side_length, start_pos[1])
    point3 = (start_pos[0] + side_length // 2, start_pos[1] - height)
    pygame.draw.polygon(screen, color, [point1, point2, point3], 2)

# Функция для рисования ромба
def draw_rhombus(start_pos, end_pos, color):
    width = abs(end_pos[0] - start_pos[0])
    height = abs(end_pos[1] - start_pos[1])
    center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
    points = [
        (center[0], center[1] - height // 2),
        (center[0] + width // 2, center[1]),
        (center[0], center[1] + height // 2),
        (center[0] - width // 2, center[1])
    ]
    pygame.draw.polygon(screen, color, points, 2)

# Основной цикл игры
running = True
start_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y <= 40:  # Проверка выбора цвета
                selected_color_index = (x - 10) // 40
                if 0 <= selected_color_index < 7:
                    current_color = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)][selected_color_index]
            else:
                start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and start_pos:
            end_pos = event.pos
            if shape_mode == 'rectangle':
                rect_width = abs(end_pos[0] - start_pos[0])
                rect_height = abs(end_pos[1] - start_pos[1])
                pygame.draw.rect(screen, current_color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), rect_width, rect_height), 2)
            elif shape_mode == 'circle':
                radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5 / 2)
                center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                pygame.draw.circle(screen, current_color, center, radius, 2)
            elif shape_mode == 'equilateral_triangle':
                draw_equilateral_triangle(start_pos, end_pos, current_color)
            elif shape_mode == 'rhombus':
                draw_rhombus(start_pos, end_pos, current_color)
            start_pos = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                shape_mode = 'rectangle'
            elif event.key == pygame.K_c:
                shape_mode = 'circle'
            elif event.key == pygame.K_b:
                shape_mode = 'brush'
            elif event.key == pygame.K_e:
                shape_mode = 'eraser'
            elif event.key == pygame.K_t:
                shape_mode = 'equilateral_triangle'
            elif event.key == pygame.K_h:
                shape_mode = 'rhombus'

    # Рисование кистью или ластиком
    if pygame.mouse.get_pressed()[0] and start_pos and shape_mode in ['brush', 'eraser']:
        pos = pygame.mouse.get_pos()
        color = WHITE if shape_mode == 'eraser' else current_color
        pygame.draw.circle(screen, color, pos, brush_size)

    # Отрисовка цветовой палитры
    draw_color_palette()
    pygame.display.flip()

# Управление:
# Прямоугольник - click R
# Круг - click C
# Кисть - click B
# Ластик - click E
# Равносторонний треугольник - click T
# Ромб -click H
